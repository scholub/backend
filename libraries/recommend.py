from pydantic import BaseModel, Field
from libraries.initalizer import db

from queries.user.get_user_by_email_async_edgeql import (GetUserByEmailResult, 
                                                         GetUserByEmailResultBookmarksItem, 
                                                         get_user_by_email)

from queries.post.get_post_async_edgeql import get_post

import math
import numpy as np
from sklearn.cluster import KMeans
import asyncio


class RecomendPostResult(BaseModel):
    paper_id : str = Field( description="The ID of the recommended paper_id.")
    similarity_score: float = Field( description="The similarity score of the recommended post." )

async def cluster_recommendations(emb_matrix: np.ndarray,
                             paper_ids: list[str],
                             top_n_per_cluster: int,
                             max_results: int) -> list[tuple[str, float]]:
    # 클러스터 개수 계산
    n_clusters = math.ceil(max_results / top_n_per_cluster)
    n_clusters = min(n_clusters, emb_matrix.shape[0])

    # 클러스터링 수행
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(emb_matrix)
    centroids = kmeans.cluster_centers_

    # 각 클러스터에서 중심점에 가장 가까운 top_n_per_cluster개의 포인트 선택
    results: list[tuple[str, float]] = []
    for cluster_idx in range(n_clusters):
        indices = [i for i, lbl in enumerate(labels) if lbl == cluster_idx]
        dists = [
            (i, np.linalg.norm(emb_matrix[i] - centroids[cluster_idx]))
            for i in indices
        ]
        dists_sorted = sorted(dists, key=lambda x: x[1])[:top_n_per_cluster]
        for idx, dist in dists_sorted:
            results.append((paper_ids[idx], float(dist)))

    # 전체 결과를 거리 기준으로 정렬한 후 최대 max_results개로 제한
    results_sorted = sorted(results, key=lambda x: x[1])[:max_results]
    return results_sorted


# 추천 함수 () -> [추천 Post id]
# - 유저의 북마크(Post 리스트)를 불러옴
# - 포스트 안의 임베딩 값을 다 가져옴
# - 다 가져와서 클러스터링을 때리고
# - 클러스터 중심점 찍고, 그 값으로 벡터 검색
# - 그리고 검색된 (post id, 유사도)를 상위 10개만 리턴

async def recomend_post(user_email: str, top_n_per_cluster: int = 3, max_results: int = 10) -> list[RecomendPostResult]: 
    res: GetUserByEmailResult = await get_user_by_email(db, email=user_email)
    bookmarks:list[GetUserByEmailResultBookmarksItem] = res.bookmarks
    if not bookmarks:
        return []

    embeddings = [np.array(item.embedding) for item in bookmarks]
    paper_ids = [item.paper_id for item in bookmarks]

    emb_matrix = np.vstack(embeddings)

    recs = await asyncio.to_thread(
        cluster_recommendations,
        emb_matrix,
        paper_ids,
        top_n_per_cluster,
        max_results
    )
    post_results = []
    for pid, score in recs:
        post = await get_post(db, paper_id=pid)
        if post:
            post_results.append(RecomendPostResult(paper_id=pid, similarity_score=score))
    
    return post_results
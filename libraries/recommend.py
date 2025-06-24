from queries.posts.search_async_edgeql import search as search_posts
from queries.user.get_user_by_email_async_edgeql import GetUserByEmailResultBookmarksItem, get_user_by_email
from queries.user import insert_recommendation, get_users
from queries.post.get_post_async_edgeql import get_post
from pydantic import BaseModel, Field
from uuid import UUID
from .initalizer import db, get_data_path

import math
import numpy as np
from sklearn.cluster import KMeans
import asyncio

class RecommendPostResult(BaseModel):
    id: UUID = Field(..., description="The internal ID of the result.")
    paper_id: str = Field(..., description="The ID of the recommended paper_id.")
    similarity_score: float = Field(..., description="Cosine similarity (높을수록 유사).")

async def recommend_post_single(
    user_email: str,
    top_n_per_cluster: int = 3,
    max_results: int = 10
) -> list[RecommendPostResult]: 
    
    # 1) 사용자 북마크 로드
    res = await get_user_by_email(db, email=user_email)
    if not res or not res.bookmarks:
        return []

    bookmarks: list[GetUserByEmailResultBookmarksItem] = res.bookmarks
    paper_ids = [b.paper_id for b in bookmarks]
    embeddings = np.vstack([np.array(b.embedding) for b in bookmarks])

    # 2) 클러스터링
    n_clusters = min(math.ceil(max_results / top_n_per_cluster), embeddings.shape[0])
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(embeddings)
    centroids = kmeans.cluster_centers_

    # 3) 각 centroid로 벡터 검색(search) 수행
    #    중복된 paper_id는 가장 높은 similarity 값으로 유지
    candidate_map: dict[str, float] = {} # {paper_id :cosine_similarity}
    for centroid in centroids:
        results = await search_posts(
            executor=db,
            embedding=centroid.tolist(),
            limit=top_n_per_cluster
        )
        for r in results:
            # 이미 북마크한 포스트는 제외
            if r.paper_id in paper_ids: continue
            sim = r.cosine_similarity

            # 중복된 ID는 더 높은 sim을 유지 (근데 아마 없을거임)
            if candidate_map.get(r.paper_id, 0) < sim:
                candidate_map[r.paper_id] = sim

    # 4) similarity 기준으로 정렬 후 max_results개 자르기
    sorted_candidates = sorted(
        candidate_map.items(),
        key=lambda x: x[1],
        reverse=True
    )[:max_results]

    # 5) Post 엔티티 조회 & RecommendPostResult 생성
    post_results: list[RecommendPostResult] = []
    for paper_id, sim in sorted_candidates:
        post = await get_post(db, paper_id=paper_id)
        if post:
            post_results.append(
                RecommendPostResult(
                    id=post.id,
                    paper_id=paper_id,
                    similarity_score=sim
                )
            )

    # 6) DB에 추천 기록 저장
    await insert_recommendation(
        db,
        email=user_email,
        recommendation=[r.id for r in post_results]
    )

    return post_results
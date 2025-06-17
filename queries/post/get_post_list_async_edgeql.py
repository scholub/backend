from __future__ import annotations
import dataclasses
import datetime
import gel
from typing import List


@dataclasses.dataclass
class GetPostListResult:
    paper_id: str
    created: datetime.datetime
    title: str
    description: str
    category: str
    tag: str
    modified: datetime.datetime
    like_count: int
    dislike_count: int

async def get_post_list(
    executor: gel.AsyncIOExecutor,
) -> List[GetPostListResult]:
    result = await executor.query(
        """\
        SELECT Paper::Post {
            paper_id,
            created,
            title,
            description,
            category,
            tag,
            modified,
            like_count,
            dislike_count
        };\
        """
    )

    return [GetPostListResult(
            paper_id=item.paper_id,
            created=item.created,
            title=item.title,
            description=item.description,
            category=item.category,
            tag=item.tag,
            modified=item.modified,
            like_count=item.like_count,
            dislike_count=item.dislike_count
        ) for item in result
    ]

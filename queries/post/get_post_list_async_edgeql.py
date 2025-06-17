from __future__ import annotations
import dataclasses
import datetime
import gel
import uuid
from typing import List


@dataclasses.dataclass
class GetPostListResult:
    id: uuid.UUID
    title: str
    description: str
    category: str
    tag: str
    created: datetime.datetime
    modified: datetime.datetime
    like_count: int
    dislike_count: int


async def get_post_list(
    executor: gel.AsyncIOExecutor,
) -> List[GetPostListResult]:

    return await executor.query(
        """\
        SELECT Paper::Post {
            id,
            title,
            description,
            category,
            tag,
            created,
            modified,
            like_count,
            dislike_count
        };\
        """
    )

# AUTOGENERATED FROM 'queries/post/reaction.edgeql' WITH:
#     $ gel-py --dir queries --no-skip-pydantic-validation


from __future__ import annotations
import dataclasses
import gel
import uuid


@dataclasses.dataclass
class ReactionResult:
    id: uuid.UUID


async def reaction(
    executor: gel.AsyncIOExecutor,
    *,
    paper_id: str,
    user_id: uuid.UUID,
    is_like: bool,
) -> ReactionResult | None:
    return await executor.query_single(
        """\
        with
          post := (select Paper::Post filter .paper_id = <str>$paper_id limit 1),
          user := (select User filter .id = <uuid>$user_id limit 1),
        insert Paper::Reaction {
          is_like := <bool>$is_like,
          user := user,
          post := post
        } unless conflict on ((.user, .post)) else (
          update Paper::Reaction filter .user = user and .post = post set {
            is_like := <bool>$is_like
          }
        );
        update Paper::Post filter .paper_id = <str>$paper_id set {
          like_count := count((select Paper::Reaction filter .post.paper_id = <str>$paper_id and .is_like = true)),
          dislike_count := count((select Paper::Reaction filter .post.paper_id = <str>$paper_id and .is_like = false))
        };\
        """,
        paper_id=paper_id,
        user_id=user_id,
        is_like=is_like,
    )

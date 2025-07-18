# AUTOGENERATED FROM 'queries/user/update_recommends.edgeql' WITH:
#     $ gel-py --dir queries


from __future__ import annotations
import dataclasses
import gel
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # Pydantic 2.x
        from pydantic_core.core_schema import any_schema
        return any_schema()

    @classmethod
    def __get_validators__(cls):
        # Pydantic 1.x
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        _ = pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class UpdateRecommendsResult(NoPydanticValidation):
    id: uuid.UUID


async def update_recommends(
    executor: gel.AsyncIOExecutor,
    *,
    recommends: list[uuid.UUID],
    email: str,
) -> UpdateRecommendsResult | None:
    return await executor.query_single(
        """\
        update User
        filter .email = <str>$email
        set {
          recommends := (
            select Paper::Post
            filter .id in array_unpack(<array<uuid>>$recommends)
          )
        };\
        """,
        recommends=recommends,
        email=email,
    )

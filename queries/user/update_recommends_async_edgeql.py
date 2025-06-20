from __future__ import annotations
import dataclasses
import gel
import uuid

from libraries.recommend import RecomendPostResult

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
class UpdateRecommnedResult(NoPydanticValidation):
    paper_id: str

async def update_recommends(
    executor: gel.AsyncIOExecutor,
    *,
    email: str,
    recommends: list[RecomendPostResult | str],
) -> UpdateRecommnedResult | None:
    return await executor.query_single(
        """\
        update User
        filter .email = <str>$email
        set {
            recommends := <array<str>>$recommends
        };
        """,
        email=email,
        recommends=recommends,
    )

from dmr import (
    Controller,
    Query,
)
from dmr.plugins.pydantic import PydanticSerializer

from .schemas import (
    DecideQuery,
    DecideResponse,
)
from .services import decide


class DecideController(Controller[PydanticSerializer]):
    async def get(self, parsed_query: Query[DecideQuery]) -> DecideResponse:
        return decide(parsed_query)

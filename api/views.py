from dmr import (
    Controller,
    Query,
    modify,
)
from dmr.plugins.pydantic import PydanticSerializer

from .schemas import (
    DecideQuery,
    DecideResponse,
)
from .services import decide


class DecideController(Controller[PydanticSerializer]):

    @modify(
        operation_id="decideDeployOrNot",
        summary="Decide whether to deploy",
        description="Returns a yes/no verdict on deploying today, with extra suspicion on Fridays.",
        tags=["decide"],
    )
    async def get(self, parsed_query: Query[DecideQuery]) -> DecideResponse:
        return decide(parsed_query)

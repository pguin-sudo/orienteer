from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.responses import Response

from orienteer.general.data.orienteer.services import transactions
from orienteer.general.utils.dtos import UserDTO
from orienteer.general.config import PLAYTIME_TOKEN

router = APIRouter()


@router.post("/api/playtime")
async def sponsor_info_handler_route(request: Request):
    request = await request.json()

    if request["token"] != PLAYTIME_TOKEN:
        return Response(status_code=401)

    await transactions.add_orientiks_from_playtime(
        user_dto=await UserDTO.from_user_id(UUID(request["user_id"])),
        minutes=request["overall"],
    )

    return Response(status_code=200)

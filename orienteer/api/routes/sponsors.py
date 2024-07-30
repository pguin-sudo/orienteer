from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from orienteer.general.data.orienteer.services import sponsors

router = APIRouter()


@router.get('/api/sponsors/{user_id}')
async def sponsor_info_handler_route(user_id: UUID):
    if not user_id or user_id == "00000000-0000-0000-0000-000000000000":
        raise HTTPException(status_code=404, detail="User not found")

    sponsor_dict = await sponsors.get_sponsor_as_dict(user_id)
    if sponsor_dict is not None:
        return JSONResponse(content=sponsor_dict)
    else:
        raise HTTPException(status_code=404, detail="Sponsor not found")

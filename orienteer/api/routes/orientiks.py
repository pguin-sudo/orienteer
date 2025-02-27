from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from orienteer.general.config import TOKEN_ORIENTIKS
from orienteer.general.data.orienteer.services.transactions import get_balance, spend
from orienteer.general.data.ss14.repositories.player import get_user_id

router = APIRouter()

@router.post("/api/orientiks")
async def handle_purchase(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {TOKEN_ORIENTIKS}":
        raise HTTPException(status_code=401, detail="[purchases]: Wrong token")

    data = await request.json()
    ckey = data.get("ckey")
    price = data.get("price")

    if not ckey or price is None:
        raise HTTPException(status_code=400, detail="[purchases]: Incorrect data")

    user_id = await get_user_id(ckey)
    if user_id is None:
        raise HTTPException(status_code=404, detail="[purchases]: No player with this ckey")

    current_balance = await get_balance(user_id)
    if current_balance < price:
        return JSONResponse(
            content={"Success": False, "Message": "Not enough money", "NewBalance": float(current_balance)},
            status_code=400
        )

    await spend(user_id, price)
    new_balance = await get_balance(user_id)

    return JSONResponse(
        content={"Success": True, "Message": "Purchase complete successfully!", "NewBalance": float(new_balance)},
        status_code=200
    )

@router.post("/api/orientiks/balance")
async def get_balance_request(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {TOKEN_ORIENTIKS}":
        raise HTTPException(status_code=401, detail="[balance]: Wrong token")

    data = await request.json()
    ckey = data.get("ckey")

    if not ckey:
        raise HTTPException(status_code=400, detail="[balance]: Incorrect data")

    user_id = await get_user_id(ckey)
    if user_id is None:
        raise HTTPException(status_code=404, detail="[balance]: No player with this ckey")

    balance = await get_balance(user_id)
    return JSONResponse(
        content={"Success": True, "Balance": float(balance)},
        status_code=200
    )
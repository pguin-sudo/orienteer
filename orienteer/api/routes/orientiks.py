from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from orienteer.general.config import ORIENTIKS_SECRET_KEY
from orienteer.general.data.orienteer.services.transactions import get_balance, spend
from orienteer.general.data.ss14.repositories.player import get_user_id

router = APIRouter()

@router.post("/api/orientiks/purchases")
async def handle_purchase(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {ORIENTIKS_SECRET_KEY}":
        raise HTTPException(status_code=401, detail="[orientiks]: Wrong token")

    data = await request.json()
    ckey = data.get("ckey")
    price = data.get("price")

    if not ckey or price is None:
        raise HTTPException(status_code=400, detail="[orientiks]: Incorrect data")

    user_id = await get_user_id(ckey)
    if user_id is None:
        raise HTTPException(status_code=404, detail="[orientiks]: No player with this ckey")

    current_balance = await get_balance(user_id)
    if current_balance < price:
        return JSONResponse(
            content={"success": False, "message": "Not enough money", "newBalance": current_balance},
            status_code=400
        )

    await spend(user_id, price)
    new_balance = await get_balance(user_id)

    return JSONResponse(
        content={"success": True, "message": "Purchase complete successfully!", "newBalance": new_balance},
        status_code=200
    )

@router.get("/api/orientiks/balance")
async def get_balance_request(ckey: str, request: Request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {ORIENTIKS_SECRET_KEY}":
        raise HTTPException(status_code=401, detail="[balance]: Wrong token")

    if not ckey:
        raise HTTPException(status_code=400, detail="[balance]: Incorrect data")

    user_id = await get_user_id(ckey)
    if user_id is None:
        raise HTTPException(status_code=404, detail="[balance]: No player with this ckey")

    balance = await get_balance(user_id)
    return JSONResponse(
        content={"success": True, "balance": balance},
        status_code=200
    )
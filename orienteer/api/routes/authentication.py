import os
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates

from orienteer.api.utils.authentication import check_linked, discord_auth_redirect, generate_auth_data


router = APIRouter()

base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, '../static/templates')
templates = Jinja2Templates(directory=templates_dir)


@router.get('/api/auth/redirect')
async def discord_auth_redirect_route(request: Request, code: str = Query(...), state: str = Query(...)):
    try:
        result = await discord_auth_redirect(code, state)
        return templates.TemplateResponse(request=request,
                                          name='success.html',
                                          context=result,
                                          status_code=200)
    except HTTPException as e:
        return templates.TemplateResponse(request=request,
                                          name='error.html',
                                          context={'message': e.detail},
                                          status_code=e.status_code)


@router.post('/api/auth/{user_id}')
async def generate_auth_data_route(user_id: UUID, key: str = Query(...)):
    return await generate_auth_data(user_id, key)


@router.get('/api/auth/{user_id}')
async def check_linked_route(user_id: UUID):
    return await check_linked(user_id)

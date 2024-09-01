import os

from fastapi import FastAPI, Request
from loguru import logger

from orienteer.api.routes.authentication import templates

app = FastAPI(template_dir=os.path.abspath('templates'))


@app.get('/tools/templates/success')
async def success(request: Request):
    return templates.TemplateResponse(request=request, name='success.html',
                                      context={'discord_name': '<дискорд юзернейм>', 'user_name': '<сс14 юзернейм>'},
                                      status_code=200)


@app.get('/tools/templates/error')
async def error(request: Request):
    return templates.TemplateResponse(request=request, name='error.html', context={
        'message': 'Аккаунт SS14, который вы пытаетесь верифицировать не существует.'}, status_code=200)


if __name__ == '__main__':
    logger.success('<<<<<<<<<<<<<<<< API module is starting >>>>>>>>>>>>>>>>')

    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=80)

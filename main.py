from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import RedirectResponse, JSONResponse
import uvicorn

from routes import author_controller
from routes import auth_controller
from sql_app import models as models
from db import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title='Library', openapi_url='/openapi.json')


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f'Failed to execute: {request.method}: {request.url}'
    return JSONResponse(status_code=400, content={'message': f'{base_error_message}. Detail: {err}'})


app.include_router(author_controller.router, prefix='/authors')
app.include_router(auth_controller.router, prefix='/auth')


if __name__ == '__main__':
    uvicorn.run('main:app', port=9000, reload=True)

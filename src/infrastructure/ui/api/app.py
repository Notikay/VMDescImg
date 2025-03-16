import uvicorn
from fastapi import FastAPI

from infrastructure.ui.api.routers import router
from infrastructure.config import FASTAPI_HOST, FASTAPI_PORT

app = FastAPI(
    title='VMDescImg API',
    description="API для получения описания изображения."
)

app.include_router(router)


def main():
    uvicorn.run(app, host=FASTAPI_HOST, port=FASTAPI_PORT)

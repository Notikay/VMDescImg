from fastapi import APIRouter

from infrastructure.ui.api.endpoints import (
    get_descript_router,
    upload_img_router
)


router = APIRouter()
router.include_router(get_descript_router)
router.include_router(upload_img_router)

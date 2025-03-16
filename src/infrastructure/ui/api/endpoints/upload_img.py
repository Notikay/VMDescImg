from typing import TYPE_CHECKING
from logging import getLogger

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse

from infrastructure.ui.api.models import UploadImgResponse
from infrastructure.db import get_session, ImageRepository
from interface_adapters.presenters import UploadImgViewer
from interface_adapters.controllers import ImgHandler
from use_cases import UploadImg

if TYPE_CHECKING:
    from infrastructure.db import Session


logger = getLogger(__name__)

router = APIRouter()


@router.post('/upload_img', response_model=UploadImgResponse)
async def upload_img(
        file: UploadFile = File(...),
        session: 'Session' = Depends(get_session)
) -> JSONResponse:
    """
    Загрузка изображения.

    :param file: Файл изображения.
    :type file: UploadFile

    :param session: Сессия подключения к БД.
    :type session: Session

    :return: Результат загрузки изображения.
    :rtype: JSONResponse

    :raises HTTPException: Если файл не является изображением.
    :raises HTTPException: Если ошибка при считывании изображения.
    :raises HTTPException: Если ошибка при загрузке изображения.
    """

    # Валидация изображения.
    if not file.content_type.startswith("image/"):
        msg = "Файл не является изображением!"
        logger.debug(msg)
        raise HTTPException(
            status_code=400,
            detail=msg
        )

    # Считывание изображения (конвертация в байты).
    try:
        img = await file.read()
    except Exception:
        msg = "Ошибка при считывании изображения!"
        logger.debug(msg)
        raise HTTPException(
            status_code=400,
            detail=msg
        )

    # Загрузка изображения.
    upload_img_result = ImgHandler(
        UploadImgViewer(),
        UploadImg(ImageRepository(session))
    ).upload(img)

    # Обработка ошибки.
    if upload_img_result.code != 200:
        logger.debug(upload_img_result.error)
        session.rollback()
        raise HTTPException(
            status_code=upload_img_result.code,
            detail=upload_img_result.msg
        )

    logger.debug(upload_img_result.msg)

    return JSONResponse(content={'uuid': upload_img_result.uuid})

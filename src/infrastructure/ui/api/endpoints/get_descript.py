from typing import TYPE_CHECKING
from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from infrastructure.ui.api.models import (
    GetDescriptRequest,
    GetDescriptResponse
)
from infrastructure.db import (
    get_session,
    ImageRepository,
    DescriptionRepository
)
from interface_adapters.presenters import GetDescriptViewer
from interface_adapters.controllers import DescriptHandler
from use_cases import GetDescript

if TYPE_CHECKING:
    from infrastructure.db import Session


logger = getLogger(__name__)

router = APIRouter()


@router.post('/get_descript', response_model=GetDescriptResponse)
async def get_descript(
        data: GetDescriptRequest,
        session: 'Session' = Depends(get_session)
) -> JSONResponse:
    """
    Получение описания изображения.

    :param data: Данные для получения описания изображения.
    :type data: GetDescriptRequest

    :param session: Сессия подключения к БД.
    :type session: Session

    :return: Результат получения описания изображения.
    :rtype: JSONResponse

    :raises HTTPException: Если ошибка при получении описания
                           изображения.
    """

    # Получение описания изображения.
    get_descript_result = DescriptHandler(
        GetDescriptViewer(),
        GetDescript(ImageRepository(session), DescriptionRepository(session))
    ).get(
        data.uuid,
        data.name_cap_model,
        data.name_translator,
        data.max_length
    )

    if get_descript_result.code != 200:
        logger.debug(get_descript_result.error)
        session.rollback()
        raise HTTPException(
            status_code=get_descript_result.code,
            detail=get_descript_result.msg
        )

    logger.debug(get_descript_result.msg)

    return JSONResponse(content={'desc': get_descript_result.desc})

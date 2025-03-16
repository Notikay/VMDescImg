from logging import getLogger
from typing import Any
from io import BytesIO

import gradio as gr

from infrastructure.db import Session, ImageRepository, DescriptionRepository
from interface_adapters.presenters import UploadImgViewer, GetDescriptViewer
from interface_adapters.controllers import ImgHandler, DescriptHandler
from use_cases import UploadImg, GetDescript

from infrastructure.config import (
    GRADIO_CAP_MODEL_NAME_MAP,
    GRADIO_TRANS_NAME_MAP,
    MIN_LENGTH_DESCRIPTION,
    MAX_LENGTH_DESCRIPTION,
    DEFAULT_LENGTH_DESCRIPTION,
    STEP_LENGTH_DESCRIPTION,
    GRADIO_HOST,
    GRADIO_PORT
)


logger = getLogger(__name__)


def get_descript(
        image: Any,
        name_cap_model: str,
        name_translator: str,
        max_length: int | None
) -> str:
    """
    Получение описания изображения.

    :param image: Изображение, описание которого нужно получить.
    :type image: Any

    :param name_cap_model: Название captioning-модели.
    :type name_cap_model: str

    :param name_translator: Название переводчика.
    :type name_translator: str

    :param max_length: Максимальная длина описания изображения.
    :type max_length: int | None

    :return: Описание изображения или ошибка при его получении.
    :rtype: str
    """

    logger.debug("Начало получения описания изображения")

    # Получение изображения в байтах.
    with BytesIO() as buff:
        try:
            image.save(buff, format="PNG")
            img = buff.getvalue()
        except Exception as e:
            logger.debug(f"Ошибка при конвертации изображения в байты: {e}!")
            return "Ошибка при конвертации изображения!"
    logger.debug("Конвертация изображения в байты прошла успешно")

    with Session() as session:

        # Загрузка изображения.
        upload_img_result = ImgHandler(
            UploadImgViewer(),
            UploadImg(ImageRepository(session))
        ).upload(img)

        # Обработка ошибки загрузки изображения.
        if upload_img_result.code != 200:
            logger.debug(upload_img_result.error)
            session.rollback()
            return upload_img_result.msg
        logger.debug("Загрузка изображения прошла успешно: "
                     f"{upload_img_result.uuid}")

        # Получение описания изображения.
        get_descript_result = DescriptHandler(
            GetDescriptViewer(),
            GetDescript(
                ImageRepository(session),
                DescriptionRepository(session)
            )
        ).get(
            upload_img_result.uuid,
            GRADIO_CAP_MODEL_NAME_MAP[name_cap_model],
            GRADIO_TRANS_NAME_MAP[name_translator],
            max_length
        )

        # Обработка результата описания изображения.
        if get_descript_result.code != 200:
            logger.debug(get_descript_result.error)
            session.rollback()
            return get_descript_result.msg
        logger.debug("Получение описания изображения прошло успешно: "
                     f"{get_descript_result.desc}")

    return get_descript_result.desc

def main() -> None:
    """ Запуск интерфейса."""

    with gr.Blocks() as ui:
        gr.Markdown("# Сервис описания изображений")

        image = gr.Image(type="pil")
        name_cap_model = gr.Dropdown(
            choices=list(GRADIO_CAP_MODEL_NAME_MAP.keys()),
            label="Captioning-модель"
        )
        name_translator = gr.Dropdown(
            choices=(list(GRADIO_TRANS_NAME_MAP.keys())),
            label="Переводчик"
        )
        max_length = gr.Slider(
            minimum=MIN_LENGTH_DESCRIPTION,
            maximum=MAX_LENGTH_DESCRIPTION,
            value=DEFAULT_LENGTH_DESCRIPTION,
            step=STEP_LENGTH_DESCRIPTION,
            label="Максимальная длина описания изображения"
        )
        result = gr.Textbox(label="Описание изображения")

        button = gr.Button("Получить описание изображения")
        button.click(
            fn=get_descript,
            inputs=[
                image,
                name_cap_model,
                name_translator,
                max_length
            ],
            outputs=result
        )

    ui.launch(server_name=GRADIO_HOST, server_port=GRADIO_PORT)

from pydantic import BaseModel, Field

from infrastructure.config import (
    BLIP_MODEL_NAME,
    CAP_MODEL_SETTINGS,
    TRANS_MODEL_SETTINGS,
    MIN_LENGTH_DESCRIPTION,
    MAX_LENGTH_DESCRIPTION
)


class GetDescriptRequest(BaseModel):
    uuid: str = Field(
        default="",
        title="UUID",
        description="UUID загруженного изображения.",
        examples=["65c45216-145b-4b9a-b78c-3fe620e9138d"]
    )
    name_cap_model: str = Field(
        default=BLIP_MODEL_NAME,
        title="Captioning-модель",
        description="Название captioning-модели, которая будет "
                    "использоваться для описания изображения.",
        examples=list(CAP_MODEL_SETTINGS.keys())
    )
    name_translator: str | None = Field(
        default=None,
        title="Переводчик",
        description="Переводчик, который будет использоваться для перевода "
                    "описания изображения.",
        examples=list(TRANS_MODEL_SETTINGS.keys())
    )
    max_length: int | None = Field(
        default=None,
        title="Максимальная длина",
        description="Максимальная длина описания изображения (при "
                    "использовании переводчика может измениться).",
        examples=[MIN_LENGTH_DESCRIPTION, MAX_LENGTH_DESCRIPTION]
    )


class GetDescriptResponse(BaseModel):
    desc: str = Field(
        default="",
        title="Результат получения описания изображения",
        description="Описание изображения или ошибка его получения.",
        examples=["Блаблабла", "Ошибка, при получении описания изображения!"]
    )

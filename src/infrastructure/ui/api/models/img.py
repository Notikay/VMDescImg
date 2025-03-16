from pydantic import BaseModel, Field


class UploadImgResponse(BaseModel):
    uuid: str = Field(
        default="",
        title="UUID",
        description="UUID загруженного изображения.",
        examples=[
            "65c45216-145b-4b9a-b78c-3fe620e9138d",
            "Ошибка, при загрузке изображения!"
        ]
    )

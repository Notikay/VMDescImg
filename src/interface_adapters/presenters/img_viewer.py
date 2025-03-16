from interface_adapters.presenters.base import AbstractViewer
from interface_adapters.presenters.dto import (
    UploadImgResponse,
    ErrorResponse
)


class UploadImgViewer(AbstractViewer):
    """ Представление результата загрузки изображения."""

    @staticmethod
    def present(uuid: str) -> UploadImgResponse:
        """
        Представление UUID запроса.

        :param uuid: UUID запроса.
        :type uuid: str

        :return: Результат представления UUID запроса.
        :rtype: UploadImgResponse
        """

        return UploadImgResponse(
            uuid=uuid,
            msg="Загрузка изображения прошла успешно!",
            code=200
        )

    @staticmethod
    def present_error(error: str, code: int) -> ErrorResponse:
        """
        Представление ошибки.

        :param error: Текст ошибки.
        :type error: str

        :param code: Код ошибки.
        :type code: int

        :return: Результат представления ошибки.
        :rtype: ErrorResponse
        """

        return ErrorResponse(
            error=error,
            msg="Ошибка, при загрузке изображения!",
            code=code
        )

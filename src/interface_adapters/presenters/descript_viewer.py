from interface_adapters.presenters.base import AbstractViewer
from interface_adapters.presenters.dto import (
    GetDescriptResponse,
    ErrorResponse
)


class GetDescriptViewer(AbstractViewer):
    """ Представление результата получения описания изображения."""

    @staticmethod
    def present(desc: str) -> GetDescriptResponse:
        """
        Представление описания изображения.

        :param desc: Описание изображения.
        :type desc: str

        :return: Результат представления описания изображения.
        :rtype: GetDescriptResponse
        """

        return GetDescriptResponse(
            desc=desc,
            msg="Получение описания изображения прошло успешно!",
            code=200
        )

    @staticmethod
    def present_error(error: str, code: int) ->ErrorResponse:
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
            msg="Ошибка, при получении описания изображения!",
            code=code
        )

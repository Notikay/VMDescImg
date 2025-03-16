from typing import TYPE_CHECKING, Union
from uuid import UUID

from infrastructure.config import (
    CAP_MODEL_SETTINGS,
    TRANS_MODEL_SETTINGS,
    MIN_LENGTH_DESCRIPTION,
    MAX_LENGTH_DESCRIPTION
)

if TYPE_CHECKING:
    from interface_adapters.presenters import AbstractViewer
    from interface_adapters.presenters.dto import (
        GetDescriptResponse,
        ErrorResponse
    )
    from use_cases import AbstractUseCase


class DescriptHandler:
    """
    Обработчик описания изображения.

    :ivar __pres: Атрибут представления описания изображения.
    :type __pres: AbstractViewer

    :ivar __get_descript: Атрибут получения описания изображения.
    :type __get_descript: GetDescript
    """

    def __init__(
            self,
            pres: 'AbstractViewer',
            get_descript: 'AbstractUseCase'
    ) -> None:
        """
        Инициализация обработчика описания изображения.

        :param pres: Представление описания изображения.
        :type pres: AbstractViewer

        :param get_descript: Получение описания изображения.
        :type get_descript: AbstractUseCase
        """

        self.__pres = pres
        self.__get_descript = get_descript

    def get(
            self,
            uuid: str,
            name_cap_model: str,
            name_translator: str | None,
            max_length: int | None
    ) -> Union['GetDescriptResponse', 'ErrorResponse']:
        """
        Получение описания изображения.

        :param uuid: UUID загруженного изображения.
        :type uuid: str

        :param name_cap_model: Название captioning-модели.
        :type name_cap_model: str

        :param name_translator: Название переводчика описания
                                изображения.
        :type name_translator: str | None

        :param max_length: Максимальная длина описания изображения.
        :type max_length: int | None

        :return: Описание изображения или ошибка.
        :rtype: GetDescriptResponse | ErrorResponse
        """

        try:
            uuid = UUID(uuid)
        except ValueError:
            return self.__pres.present_error(
                error=f"UUID {uuid} некорректный!",
                code=400
            )

        if name_cap_model not in CAP_MODEL_SETTINGS.keys():
            return self.__pres.present_error(
                error=f"Captioning-модели с именем {name_cap_model} не "
                      "существует!",
                code=400
            )

        if (name_translator is not None) and (name_translator not in
                                              TRANS_MODEL_SETTINGS.keys()):
            return self.__pres.present_error(
                error=f"Переводчик с именем {name_translator} не "
                      "существует!",
                code=400
            )

        if (max_length is not None) and (max_length < MIN_LENGTH_DESCRIPTION or
                                         max_length > MAX_LENGTH_DESCRIPTION):
            return self.__pres.present_error(
                error="Максимальная длина описания должна быть больше "
                      f"{MIN_LENGTH_DESCRIPTION} и меньше "
                      f"{MAX_LENGTH_DESCRIPTION} символов!",
                code=400
            )

        try:
            result = self.__get_descript.execute(
                uuid,
                name_cap_model,
                name_translator,
                max_length
            )
        except Exception as e:
            return self.__pres.present_error(error=str(e), code=500)

        return self.__pres.present(result)

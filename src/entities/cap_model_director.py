from typing import TYPE_CHECKING

from entities.base import AbstractCapModelDirector
from entities.translators import AbstractTranslator

if TYPE_CHECKING:
    from entities.cap_models import AbstractCapModelBuilder


class CapModelDirector(AbstractCapModelDirector):
    """
    Директор строителей captioning-моделей.

    :ivar __builder: Атрибут строителя captioning-модели.
    :type __builder: AbstractCapModelBuilder
    """

    def __init__(self, builder: 'AbstractCapModelBuilder'):
        """
        Инициализация директора captioning-моделей.

        :param builder: Строитель captioning-модели.
        :type builder: AbstractCapModelBuilder
        """

        self.__builder = builder
        self.__translator: AbstractTranslator | None = None

    def set_translator(self, translator: AbstractTranslator | None) -> None:
        """
        Назначение переводчика описания изображения.

        :param translator: Переводчик описания изображения.
        :type translator: AbstractTranslator | None

        :raises TypeError: Если тип переводчика описания изображения
                           неверен.
        """

        if translator is not None and not isinstance(translator, AbstractTranslator):
            raise TypeError("Неверный тип переводчика описания изображения!")
        self.__translator = translator

    def get_descript(self, img: bytes, max_length: int | None) -> str:
        """
        Получение описания изображения.

        :param img: Изображение.
        :type img: bytes

        :param max_length: Максимальная длина описания изображения.
        :type max_length: int | None

        :return: Описание изображения.
        :rtype: str
        """

        # Инициализация строителя captioning-модели.
        if max_length is not None:
            self.__builder.set_max_length(max_length)
        model = self.__builder.get_model()

        # Получение результата описания изображения.
        result = model.descript(img)

        # Проверка перевода результата описания изображения.
        if self.__translator is not None:
            result = self.__translator.translate(result)

        return result

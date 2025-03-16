from typing import Protocol

from entities.translators.base import AbstractTranslator


class Translator(Protocol):

    def translate(self, text: str) -> str: ...


class AppTranslator(AbstractTranslator):
    """
    Переводчик описания изображения.

    :ivar __translator: Атрибут переводчика, на который будет
                        переводиться описание изображения.
    :type __translator: TranslatorProtocol

    ::ivar __support_langs: Атрибут списка поддерживаемых языков
                            перевода.
    :type __support_langs: list[str]
    """

    def __init__(
            self,
            translator: Translator,
            support_langs: list[str]
    ) -> None:
        """
        Инициализация Переводчика.

        :param translator: Атрибут переводчика, на который будет
                           переводиться описание изображения.
        :type translator: TranslatorProtocol

        :param support_langs: Список поддерживаемых языков.
        :type support_langs: list[str]
        """

        self.__translator = translator
        self.__support_langs = support_langs

    def set_lang(self, value: str) -> None:
        """
        Назначение языка, на который будет переводиться описание
        изображения.

        :param value: Язык, на который будет переводиться описание
                      изображения.
        :type value: str

        :raises Exception: Переводчик не поддерживает смену языка.
        """

        raise Exception("Переводчик не поддерживает смену языка!")

    def translate(self, desc: str) -> str:
        """
        Перевод описания изображения.

        :param desc: Описание изображения, которое нужно перевести.
        :type desc: str

        :return: Переведенное описание изображения.
        :rtype: str
        """

        try:
            result = self.__translator.translate(text=desc)
        except Exception as e:
            raise Exception(f"Ошибка при переводе описания изображения: {e}!")

        return result

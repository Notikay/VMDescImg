import asyncio
from typing import Any

from entities.translators.base import AbstractTranslator


class GoogleTranslator(AbstractTranslator):
    """
    Google-переводчик описания изображения.

    :ivar __translator: Атрибут переводчика, на который будет
                        переводиться описание изображения.
    :type __translator: Any

    :ivar __to_lang: Атрибут языка, на который нужно перевести описание
                  изображения.
    :type __to_lang: str

    ::ivar __support_langs: Атрибут списка поддерживаемых языков
                            перевода.
    :type __support_langs: list[str]
    """

    def __init__(
            self,
            translator: Any,
            to_lang: str,
            support_langs: list[str]
    ) -> None:
        """
        Инициализация Google-переводчика.

        :param translator: Атрибут переводчика, на который будет
                           переводиться описание изображения.
        :type translator: Any

        :param to_lang: Язык, на который будет переводиться описание
                     изображения.
        :type to_lang: str

        :param support_langs: Список поддерживаемых языков.
        :type support_langs: list[str]
        """

        self.__translator = translator
        self.__to_lang = to_lang
        self.__support_langs = support_langs

    def set_lang(self, value: str) -> None:
        """
        Назначение языка, на который будет переводиться описание
        изображения.

        :param value: Язык, на который будет переводиться описание
                      изображения.
        :type value: str

        :raises TypeError: Если язык не является строкой.
        :raises ValueError: Если язык не поддерживается
                            Google-переводчиком.
        """

        if not isinstance(value, str):
            raise TypeError('Язык должен быть строкой!')
        elif not value in self.__support_langs:
            raise ValueError(f'Язык {value} не поддерживается '
                             f'Google-переводчиком!')
        self.__to_lang = value

    def translate(self, desc: str) -> str:
        """
        Перевод описания изображения.

        :param desc: Описание изображения, которое нужно перевести.
        :type desc: str

        :return: Переведенное описание изображения.
        :rtype: str
        """

        # TODO: Исправить проблему перевода через раз.

        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        try:
            # result = loop.run_until_complete(
            #     self.__translator.translate(
            #         text=desc, dest=self.__lang
            #     )
            # )
            result = asyncio.run(self.__translator.translate(
                text=desc, dest=self.__to_lang
            ))
        except Exception as e:
            raise Exception(f"Ошибка при переводе описания изображения: {e}!")
        # finally:
        #     loop.close()

        return result.text

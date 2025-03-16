from abc import ABC, abstractmethod


class AbstractTranslator(ABC):

    @abstractmethod
    def set_lang(self, value: str) -> None:
        pass

    @abstractmethod
    def translate(self, text: str) -> str:
        pass

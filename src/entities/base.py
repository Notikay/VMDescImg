from abc import ABC, abstractmethod


class AbstractCapModelDirector(ABC):

    @abstractmethod
    def set_translator(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def get_descript(self, img: bytes, max_length: int) -> str:
        pass

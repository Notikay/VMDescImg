from abc import ABC, abstractmethod


class AbstractCapModel(ABC):

    @abstractmethod
    def descript(self, img: bytes) -> str:
        pass


class AbstractCapModelBuilder(ABC):

    @abstractmethod
    def set_max_length(self, value: int) -> None:
        pass

    @abstractmethod
    def get_model(self, *args, **kwargs) -> AbstractCapModel:
        pass

from abc import abstractmethod
from typing import Any
from io import BytesIO

from PIL import Image

from entities.cap_models.base import (
    AbstractCapModel,
    AbstractCapModelBuilder
)
from infrastructure.config import DEFAULT_LENGTH_DESCRIPTION


class AbstractBLIBCapModelBuilder(AbstractCapModelBuilder):

    @abstractmethod
    def set_download_path(self, value: str) -> None:
        pass

    @abstractmethod
    def set_cache_dir(self, value: str) -> None:
        pass


class BLIPCapModel(AbstractCapModel):
    """
    Общая BLIP captioning-модель.

    :ivar __model: Атрибут captioning-модели.
    :type __model: Any

    :ivar __processor: Атрибут обработчика изображений.
    :type __processor: Any

    :ivar __max_length: Атрибут максимальной длины описания изображения.
    :type __max_length: int
    """

    def __init__(self, model: Any, processor: Any, max_length: int) -> None:
        """
        Инициализация общей BLIP captioning-модели.

        :param model: Captioning-модель.
        :type model: Any

        :param processor: Обработчик изображений.
        :type processor: Any

        :param max_length: Максимальная длина описания изображения.
        :type max_length: int
        """

        self.__model = model
        self.__processor = processor
        self.__max_length = max_length

    def descript(self, img: bytes) -> str:
        """
        Генерация описания изображения.

        :param img: Изображение.
        :type img: bytes

        :return: Описание изображения.
        :rtype: str
        """

        img = Image.open(BytesIO(img)).convert('RGB')
        proc_images = self.__processor(img, return_tensors="pt")
        batch = self.__model.generate(
            **proc_images, max_length=self.__max_length
        )
        result = self.__processor.batch_decode(
            batch, skip_special_tokens=True
        )[0]  # Описание на английском

        return result


class BLIPCapModelBuilder(AbstractBLIBCapModelBuilder):
    """
    Строитель BLIP captioning-модели.

    :ivar __model: Атрибут captioning-модели.
    :type __model: Any

    :ivar __processor: Атрибут обработчика изображений.
    :type __processor: Any

    :ivar __download_path: Атрибут пути к папке предобученных моделей.
    :type __download_path: str

    :ivar __cache_dir: Атрибут пути к папке кеша предобученных моделей.
    :type __cache_dir: str | None

    :ivar __max_length: Атрибут максимальной длины описания изображения.
    :type __max_length: int
    """

    def __init__(
            self,
            model: Any,
            processor: Any,
            download_path: str,
            cache_dir: str | None
    ) -> None:
        """
        Инициализация строителя общей BLIP captioning-модели.

        :param model: Captioning-модель.
        :type model: Any

        :param processor: Обработчик изображений.
        :type processor: Any

        :param download_path: Путь к папке предобученных моделей.
        :type download_path: str

        :param cache_dir: Путь к папке кеша предобученных моделей.
        :type cache_dir: str | None
        """

        self.__model = model
        self.__processor = processor
        self.__download_path = download_path
        self.__cache_dir = cache_dir

        self.__max_length = DEFAULT_LENGTH_DESCRIPTION

    def set_download_path(self, value: str) -> None:
        """
        Назначение пути к папке предобученных моделей.

        :param value: Путь к папке предобученных моделей.
        :type value: str

        :raises TypeError: Если путь к папке предобученных моделей не
                           является строкой.
        """

        if not isinstance(value, str):
            raise TypeError("Путь к папке предобученных моделей должен быть "
                            "строкой.")
        self.__download_path = value

    def set_cache_dir(self, value: str) -> None:
        """
        Назначение пути к папке кеша предобученных моделей.

        :param value: Путь к папке кеша предобученных моделей.
        :type value: str

        :raises TypeError: Если путь к папке кеша предобученных моделей
                           не является строкой.
        """

        if not isinstance(value, str):
            raise TypeError("Путь к папке кеша предобученных моделей должен "
                            "быть строкой.")
        self.__cache_dir = value

    def set_max_length(self, value: int) -> None:
        """
        Назначение максимальной длины описания изображения.

        :param value: Значение длины описания изображения.
        :type value: int

        :raises TypeError: Если максимальная длина описания изображения
                           не является целым числом.
        :raises ValueError: Если максимальная длина описания
                            изображения меньше 1 символа.
        """

        if not isinstance(value, int):
            raise TypeError("Максимальная длина описания изображения должна "
                            "быть целым числом.")
        elif value < 1:
            raise ValueError("Максимальная длина описания изображения должна "
                             "быть больше 1 символа.")
        self.__max_length = value

    def get_model(self) -> BLIPCapModel:
        """
        Получение captioning-модели.

        :return: Captioning-модель.
        :rtype: BLIPCapModel
        """

        cap_model = self.__model.from_pretrained(
            self.__download_path,
            cache_dir=self.__cache_dir
        )
        cap_processor = self.__processor.from_pretrained(
            self.__download_path,
            cache_dir=self.__cache_dir
        )

        return BLIPCapModel(
            cap_model,
            cap_processor,
            self.__max_length
        )

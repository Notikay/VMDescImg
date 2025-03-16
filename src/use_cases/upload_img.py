from typing import TYPE_CHECKING
from uuid import uuid4

from use_cases.base import AbstractUseCase
from infrastructure.config import PATH_TO_IMG_DIR

if TYPE_CHECKING:
    from uuid import UUID

    from infrastructure.db import AbstractImageRepository


class UploadImg(AbstractUseCase):
    """
    Загрузка изображения.

    :ivar __img_repos: Атрибут репозитория изображений, для доступа к
                       хранилищу.
    :type __img_repos: ImageRepository
    """

    def __init__(self, img_repos: 'AbstractImageRepository') -> None:
        """
        Инициализация загрузки изображения.

        :param img_repos: Репозиторий изображений, для доступа к
                          хранилищу.
        :type img_repos: ImageRepository
        """

        self.__img_repos = img_repos

    def execute(self, img: bytes) -> 'UUID':
        """
        Сохранение изображения.

        Сохранение изображения в папку, а путь к этой папке в
        хранилище, через репозиторий.

        :param img: Изображение.
        :type img: bytes

        :return: UUID загруженного изображения.
        :rtype: UUID

        :raises PermissionError: Если нет прав для сохранения
                                 изображения.
        :raises OSError: Если невозможно сохранить изображение.
        :raises Exception: Если неизвестная ошибка при сохранении
                           изображения.
        """

        # Сохранение изображения.
        path = PATH_TO_IMG_DIR.joinpath(str(hash(img)))

        try:
            with open(path, 'wb') as f:
                f.write(img)
        except PermissionError:
            raise PermissionError("Нет прав для сохранения изображения!")
        except OSError:
            raise OSError("Невозможно сохранить изображение!")
        except Exception as e:
            raise Exception(f"Неизвестная ошибка при сохранении изображения:"
                            f" {e}!")

        # Запись UUID загруженного изображения в хранилище.
        uuid = uuid4()
        self.__img_repos.set_path_with_uuid(uuid, path)

        return uuid

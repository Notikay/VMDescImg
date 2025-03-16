from logging import getLogger
from typing import TYPE_CHECKING
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from infrastructure.db.orm import RequestORM
from infrastructure.db.repositories.base import AbstractImageRepository

if TYPE_CHECKING:
    from uuid import UUID


logger = getLogger(__name__)


class ImageRepository(AbstractImageRepository):
    """
    Репозиторий изображения.

    :ivar __session: Атрибут сессии подключения к БД.
    :type __session: Session
    """

    def __init__(self, session: Session) -> None:
        """
        Инициализация репозитория изображения.

        :param session: Сессия подключения к БД.
        :type session: Session
        """

        self.__session = session

    def set_session(self, session: Session) -> None:
        """
        Установка сессии подключения к БД.

        :param session: Сессия подключения к БД.
        :type session: Session
        """

        if not isinstance(session, Session):
            raise TypeError("Сессия подключения к БД не типа Session!")

        self.__session = session

    def get_path_by_uuid(self, uuid: 'UUID') -> Path:
        """
        Получение пути к изображению по UUID запроса.

        :param uuid: UUID запроса.
        :type uuid: UUID

        :return: Путь к изображению.
        :rtype: Path

        :raises SQLAlchemyError: Если сбой при получении пути к
                                 изображению из БД.
        :raises NoResultFound: Если нет записи в БД.
        """

        try:
            result = self.__session.get(RequestORM, str(uuid))
        except Exception as e:
            msg = ("Ошибка при получении пути к изображению из "
                   f"БД по UUID запроса: {uuid}!")
            logger.error(f"{msg} - {e}")
            raise SQLAlchemyError(msg)
        if result is None:
            msg = f"Нет записи в БД о запросе с UUID: {uuid}!"
            logger.error(msg)
            raise SQLAlchemyError(msg)

        return Path(str(result.path))


    def set_path_with_uuid(self, uuid: 'UUID', path: Path) -> None:
        """
        Запись пути к изображению по UUID запроса в БД.

        :param uuid: UUID запроса.
        :type uuid: UUID

        :param path: Путь к изображению в файловой системе.
        :type path: Path

        :raises SQLAlchemyError: Если сбой при записи пути к
                                 изображению в БД.
        """

        try:
            self.__session.add(RequestORM(
                uuid=str(uuid),
                path=str(path),
                description=None
            ))
            self.__session.commit()
        except Exception as e:
            msg = ("Ошибка при записи пути к изображению в БД "
                   f"по UUID запроса: {uuid}!")
            logger.error(f"{msg} - {e}")
            raise SQLAlchemyError(msg)

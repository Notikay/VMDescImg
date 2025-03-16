from logging import getLogger
from typing import TYPE_CHECKING

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from infrastructure.db.orm import RequestORM
from infrastructure.db.repositories.base import (
    AbstractDescriptionRepository
)

if TYPE_CHECKING:
    from uuid import UUID


logger = getLogger(__name__)


class DescriptionRepository(AbstractDescriptionRepository):
    """
    Репозиторий описания изображения.

    :ivar __session: Атрибут сессии подключения к БД.
    :type __session: Session
    """

    def __init__(self, session: Session) -> None:
        """
        Инициализация репозитория описания изображения.

        :param session: Сессия подключения к БД.
        :type session: Session

        :raises TypeError: Если сессия подключения к БД не типа Session.
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


    def set_description_by_uuid(self, uuid: 'UUID', desc: str) -> None:
        """
        Запись описания изображения по UUID запроса в БД.

        :param uuid: UUID запроса.
        :type uuid: UUID

        :param desc: Описание изображения.
        :type desc: str

        :raises SQLAlchemyError: Если не удалось записать описание
                                 изображения в БД.
        :raises SQLAlchemyError: Если не найдена запрашиваемая запись с UUID
                                 запроса в БД.
        """

        stmt = (
            update(RequestORM)
            .where(RequestORM.uuid == str(uuid))
            .values(description=desc)
        )

        try:
            result = self.__session.execute(stmt)
            self.__session.commit()
        except Exception as e:
            msg = ("Ошибка при записи описания изображения в БД"
                   f"по UUID запроса: {uuid}!")
            logger.error(f"{msg} - {e}")
            raise SQLAlchemyError(msg)

        if result.rowcount == 0:
            raise SQLAlchemyError(f"Нет записи в БД о запросе с UUID: {uuid}!")

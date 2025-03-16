from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from uuid import UUID
    from pathlib import Path

    from sqlalchemy.orm import Session


class AbstractRepository(ABC):

    @abstractmethod
    def set_session(self, session: 'Session') -> None:
        pass


class AbstractImageRepository(AbstractRepository):

    @abstractmethod
    def get_path_by_uuid(self, uuid: 'UUID') -> 'Path':
        pass

    @abstractmethod
    def set_path_with_uuid(self, uuid: 'UUID', path: 'Path') -> None:
        pass


class AbstractDescriptionRepository(AbstractRepository):

    @abstractmethod
    def set_description_by_uuid(self, uuid: 'UUID', desc: str) -> None:
        pass

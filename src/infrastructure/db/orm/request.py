from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db.orm.base import Base


class RequestORM(Base):
    """ ORM для запросов."""

    __tablename__ = 'requests'

    uuid: Mapped[str] = mapped_column(
        primary_key=True,
        nullable=False,
        unique=True
    )
    path: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

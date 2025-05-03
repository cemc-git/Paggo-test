from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime

class Base(DeclarativeBase):
    pass

class Signal(Base):
    __tablename__ = "signal"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    data: Mapped[str] = mapped_column(String(30))
    timestamp: Mapped[datetime.datetime]
    signal_id: Mapped[str] = mapped_column(String(30))
    value: Mapped[float]


import datetime
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped

class Base(DeclarativeBase):
    pass

class Data(Base):
    __tablename__ = "data"
    timestamp: Mapped[datetime.datetime] = mapped_column(primary_key=True)
    wind_speed: Mapped[float]
    power: Mapped[float]
    ambient_temperature: Mapped[float]
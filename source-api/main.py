from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
from models import Data
from datetime import datetime


SOURCE_URL = "postgresql://paggo:paggo123@postgres-db-source:5432/source"
ENGINE = create_engine(SOURCE_URL)


def get_session():
    with Session(ENGINE) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

@app.get("/data")
def get_data_from_timestamp(
    date: str,
    session: SessionDep,
    wind_speed: bool = True,
    power: bool = True,
    ambient_temperature: bool = True
):
    try:
        date_time = datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        return "Formatação de dia inválida, utilize essa como exemplo: DD-MM-AA"
    
    start = date_time
    end = date_time.replace(hour=23, minute=59, second=59)
    
    data_to_fetch = [Data.timestamp]
    if wind_speed:
        data_to_fetch.append(Data.wind_speed)
    if power:
        data_to_fetch.append(Data.power)
    if ambient_temperature:
        data_to_fetch.append(Data.ambient_temperature)

    func = select(*data_to_fetch).where(
        Data.timestamp.between(start, end)
    )
    result = session.execute(func).fetchall()
    
    return [dict(row._mapping) for row in result]

   
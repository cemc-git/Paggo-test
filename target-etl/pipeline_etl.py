import asyncio
import os
from functools import partial
from typing import Callable, List, Union
from dask import bag as db
from datetime import datetime, timedelta
import pandas as pd
from etl import SourceApiClient
from create_table import create_signal_table_if_not_exists
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_target import Signal
from models import SIGNALCOLUMNS, DATACOLUMNS

def generate_dates(start_date: str, days: int = 10) -> List[str]:
    """Retorna um conjunto de datas após a data fornecida já no formato da API. Padrão de 10 datas"""
    base = datetime.strptime(start_date, "%d-%m-%Y")
    return [(base + timedelta(days=i)).strftime("%d-%m-%Y") for i in range(days)]


def process_date(date_str: str, etl: SourceApiClient) -> None:
    engine = create_engine("postgresql://paggo:paggo123@postgres-db-target:5432/target")
    Session = sessionmaker(bind=engine)
    session = Session()
    asyncio.run(fetch_and_store_wind_data(date_str, etl, session))
    asyncio.run(fetch_and_store_power_data(date_str, etl, session))


async def fetch_and_store_power_data(date_str: str, etl: SourceApiClient, session) -> None:
    print(f"Processando: {date_str}")
    wind_data = await etl.get_power_info_from_date(date_str)
    df = pd.DataFrame(wind_data)
    if DATACOLUMNS.TIMESTAMP in df.columns:
        df[DATACOLUMNS.TIMESTAMP] = pd.to_datetime(df[DATACOLUMNS.TIMESTAMP])
    else:
        print(f"[Erro] Coluna {DATACOLUMNS.TIMESTAMP} não encontrada para a data {date_str}")
        print(df.head())
        return

    df[DATACOLUMNS.TIMESTAMP] = pd.to_datetime(df[DATACOLUMNS.TIMESTAMP])
    df.set_index(DATACOLUMNS.TIMESTAMP, inplace=True)

    grouped = df[DATACOLUMNS.POWER].resample('10min').agg(['mean', 'min', 'max', 'std'])

    try:
        for ts, row in grouped.iterrows():
            interval_index = ts.hour * 6 + ts.minute // 10 + 1
            signal_id = f"power_{ts.day:02d}{ts.month:02d}{ts.year}_{interval_index:04d}"

            metrics = {
                'mean': row['mean'],
                'min': row['min'],
                'max': row['max'],
                'std': row['std'],
            }
            for metric_name, value in metrics.items():
                signal = {
                    SIGNALCOLUMNS.NAME: DATACOLUMNS.POWER,
                    SIGNALCOLUMNS.DATA: metric_name,
                    SIGNALCOLUMNS.TIMESTAMP: ts,
                    SIGNALCOLUMNS.SIGNAL_ID: signal_id,
                    SIGNALCOLUMNS.VALUE: float(value)
                }
                session.add(Signal(**signal))
            session.commit()

    except Exception as e:
        session.rollback()
        print(f"Erro ao salvar {date_str}: {e}")
    finally:
        session.close()


async def fetch_and_store_wind_data(date_str: str, etl: SourceApiClient, session) -> None:
    print(f"Processando: {date_str}")
    wind_data = await etl.get_wind_speed_info_from_date(date_str)
    df = pd.DataFrame(wind_data)
    if DATACOLUMNS.TIMESTAMP in df.columns:
        df[DATACOLUMNS.TIMESTAMP] = pd.to_datetime(df[DATACOLUMNS.TIMESTAMP])
    else:
        print(f"[Erro] Coluna {DATACOLUMNS.TIMESTAMP} não encontrada para a data {date_str}")
        print(df.head())
        return

    df[DATACOLUMNS.TIMESTAMP] = pd.to_datetime(df[DATACOLUMNS.TIMESTAMP])
    df.set_index(DATACOLUMNS.TIMESTAMP, inplace=True)

    grouped = df[DATACOLUMNS.WIND_SPEED].resample('10min').agg(['mean', 'min', 'max', 'std'])

    try:
        for ts, row in grouped.iterrows():
            interval_index = ts.hour * 6 + ts.minute // 10 + 1
            signal_id = f"{DATACOLUMNS.WIND_SPEED}_{ts.day:02d}{ts.month:02d}{ts.year}_{interval_index:04d}"

            metrics = {
                'mean': row['mean'],
                'min': row['min'],
                'max': row['max'],
                'std': row['std'],
            }
            for metric_name, value in metrics.items():
                signal = {
                    SIGNALCOLUMNS.NAME: DATACOLUMNS.WIND_SPEED,
                    SIGNALCOLUMNS.DATA: metric_name,
                    SIGNALCOLUMNS.TIMESTAMP: ts,
                    SIGNALCOLUMNS.SIGNAL_ID: signal_id,
                    SIGNALCOLUMNS.VALUE: float(value)
                }
                session.add(Signal(**signal))
            session.commit()

    except Exception as e:
        session.rollback()
        print(f"Erro ao salvar {date_str}: {e}")
    finally:
        session.close()


def run_etl_pipeline_for_dates(process_date: Callable, etl: SourceApiClient, dates: Union[str, List[str]]) -> None:
    """Método que executa o pipeline ETL para uma ou mais datas fornecidas."""
    if isinstance(dates, str):
        dates = [dates]
    process_with_etl = partial(process_date, etl=etl)
    etl_bag = db.from_sequence(dates)
    etl_bag.map(process_with_etl).compute()


if __name__ == "__main__":
    # Lê a data a partir de uma variável de ambiente
    date_input = os.getenv("DATE_INPUT", "08-05-2025")  # Valor padrão se a variável de ambiente não for definida
    etl = SourceApiClient()
    create_signal_table_if_not_exists()
    run_etl_pipeline_for_dates(process_date, etl, date_input)

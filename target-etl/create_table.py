from sqlalchemy import create_engine, inspect
from db_target import Signal

DATABASE_URL = "postgresql://paggo:paggo123@postgres-db-target:5432/target"

engine = create_engine(DATABASE_URL)


def create_signal_table_if_not_exists():
    inspector = inspect(engine)
    if 'signal' not in inspector.get_table_names():
        print("Criando tabela signal")
        Signal.metadata.create_all(engine)
    else:
        print("Tabela já existe.")
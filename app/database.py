import databases
import sqlalchemy

from .config import config

metadata = sqlalchemy.MetaData()


user_table = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

client_table = sqlalchemy.Table(
    "client",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("panel_name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("active", sqlalchemy.Boolean, default=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=sqlalchemy.func.now()),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("user.id"), nullable=False),
    sqlalchemy.Column("effective_start_at", sqlalchemy.Date),
    sqlalchemy.Column("effective_end_at", sqlalchemy.Date),
)


connect_args = {"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {}
engine = sqlalchemy.create_engine(config.DATABASE_URL, connect_args=connect_args)

metadata.create_all(engine)

db_args = {"min_size": 1, "max_size": 3} if "postgres" in config.DATABASE_URL else {}
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLLBACK, **db_args
)

print("-" * 20)
print(config.DATABASE_URL)
print()

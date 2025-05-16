from sqlalchemy import create_engine, text
from config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
    pool_size=10,
    max_overflow=10,
)

with engine.connect() as connection:
    res = connection.execute(text('SELECT VERSION()'))
    print(res.all())

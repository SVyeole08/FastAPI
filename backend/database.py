import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.environ["postgresql://product_pg_user:t01EpaZuJntkZj7yE83Uzg9T4kRPUHRv@dpg-dbcu7pdg1s2s73eice7g-a/product_pg"]

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

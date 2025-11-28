from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from commons.models.models import Base
import os.path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BANCO = os.path.join(ROOT, "data", "mercado.db")

os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)

engine = create_engine(f"sqlite:///{BANCO}")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
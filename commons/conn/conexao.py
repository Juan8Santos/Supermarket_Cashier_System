from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from commons.models.models import Base
import os.path

DIR = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(DIR, "data", "mercado.db")

os.makedirs(os.path.join(DIR, "data"), exist_ok=True)

engine = create_engine(f"sqlite:///{BANCO}")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
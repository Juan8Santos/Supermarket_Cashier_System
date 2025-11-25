from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os.path

BANCO = "mercado.db"
DIR = os.path.dirname(__file__)
BANCO = os.path.join(DIR, BANCO)

engine = create_engine("sqlite:///" + BANCO)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
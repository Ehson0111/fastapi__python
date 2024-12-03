from sqlalchemy.orm import  Session
from sqlalchemy import * 

class DBSetting():
    @staticmethod
    def get_session():
        engine=create_engine(f"postgresql+psycopg2://postgres:Novosibirsk22@localhost:5432/fastapi")
        return Session(bind=engine)
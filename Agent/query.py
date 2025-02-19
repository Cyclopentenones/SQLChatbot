from sqlalchemy.orm import Session
from Database.ORM import KHOA,  MONHOC, DIEUKIEN, GIAOVIEN, LOP, HOCVIEN, GIANGDAY, KETQUATHI
from Database.database_connection import Database

class QueryHandler:
    def __init__(self, DATABASE_URL: str):
        self.database = Database(DATABASE_URL=DATABASE_URL) 
        self.db = next(self.database.get_db()) 
        self.models = {
            "KHOA": KHOA,
            "MONHOC": MONHOC,
            "DIEUKIEN": DIEUKIEN,
            "GIAOVIEN": GIAOVIEN,
            "LOP": LOP,
            "HOCVIEN":  HOCVIEN,
            "GIANGDAY": GIANGDAY,
            "KETQUATHI": KETQUATHI
        }

    def get_table(self, type: str):
        return self.db.query(self.models[type]).all()

    def get_engine(self):
        return self.database.get_engine()

    def close(self):
        self.db.close()

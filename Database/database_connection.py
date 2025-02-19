from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect, MetaData, Table


class Database:
    def __init__(self, DATABASE_URL: str):
        self.db = None
        # Connection to SQL Server
        self.engine = create_engine(DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_engine(self):
        return self.engine

    def close(self):
        if self.db:
            self.db.close()

def main(): 
    db_instance = Database(DATABASE_URL="Link database của mày")
    with db_instance.engine.connect() as connection:
        inspector = inspect(db_instance.engine)
        tables = inspector.get_table_names()
        print("Danh sách các bảng trong database:", tables)

        metadata = MetaData()
        metadata.reflect(bind=db_instance.engine)

        for table_name in tables:
            table = Table(table_name, metadata, autoload_with=db_instance.engine)
            print(f"\nThông tin chi tiết của bảng {table_name}:")
            for column in table.columns:
                print(f" - {column.name} ({column.type})")

            query = text(f"SELECT * FROM {table_name}")
            result = connection.execute(query)
            rows = result.fetchall()
            print(f"Dữ liệu mẫu từ bảng {table_name}:")
            for row in rows:
                print(row)

if __name__ == "__main__": 
    main()
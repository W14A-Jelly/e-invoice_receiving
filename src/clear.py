from src.database import Database


def clear():
    Database.drop_tables()
    Database.create_tables()
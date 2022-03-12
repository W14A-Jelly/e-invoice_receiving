from database import Database

# Clears all data from SQLite database


def clear():
    Database.drop_tables()

import sqlite3

# Clears all data from the user table in SQLite database
def clear():
    try:
        connection = sqlite3.connect('Db.db')
        cursor = connection.cursor()
        query = "DELETE FROM Users"
        cursor.execute(query)
        connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if connection:
            connection.close()
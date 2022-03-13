from src.database import Database


def clear():
    Database.drop_tables()
    Database.create_tables()


if __name__ == "__main__":
    Database.start()
    clear()
    Database.create_tables()
    login_data = {'password': 'password',
                  'email': 'exmaple2@gmail.com',
                  'session_id': '0 1',
                  'user_id': 1}

    Database.insert('Login', login_data)
    Database.print_table('Login')
    Database.insert('Ownership', {'user_id': 1, 'xml_id': 123})
    Database.print_table('Ownership')
    clear()
    Database.create_tables()
    Database.print_table('Login')
    Database.print_table('Ownership')

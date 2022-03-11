from schema import db, Login, Email, Ownership

'''
Database class to manipulate table data and connect to SQLite server

Arguments:
    table (string) - table name e.g 'Login', 'Email' or 'Ownership'
    id (integer) - Existing User id that correspond to a record in a table
    data (dictionary) - e.g {'password' : 'password',
                            'email' : 'exmaple@gmail.com', 
                            'session_id' : '0 1',
                            'user_id' : 0}

Usecase:
    Database.start()
    Database.create_tables()
    Database.insert('Login', {'password' : 'password',
                                'email' : 'exmaple@gmail.com', 
                                'session_id' : '0 1',
                                'user_id' : 0})
    Database.update('Login', 0, {'password' :'newpassword',
                                    'email' : 'new@gmail.com'})
    Database.close()
'''

def find_table(table):
    match table:
        case 'Login':
            return Login
        case 'Email':
            return Email
        case 'Ownership':
            return Ownership

class Database:
    def start():
        # Connect to SQLite server. Error if server is already connected.
        db.connect()

    def stop():
        # Disconnect from SQLite server if connected.
        db.close()

    def create_tables():
        # Create new tables defined in schema.py if tables not exist.
        db.create_tables([Login, Email, Ownership], safe=True)

    def drop_tables():
        # Delete all existing tables if tables exist.
        db.drop_tables([Login, Email, Ownership], safe=True)

    def insert(table, data):
        # Insert or bulk insert a new record into a table
        table = find_table(table)
        table.insert_many(data).execute()

    def update(table, id, data):
        # Update existing record in a table via user_id
        table = find_table(table)
        table.update(data).where(table.user_id==id).execute()

    def num_rows(table):
        # Return the number of records in a table
        table = find_table(table)
        return(table.select().count())

    def print_table(table):
        # For debugging purposes
        name = table
        table = find_table(table)
        symb = '-'
        num_symb = 20

        print(symb * int(num_symb / 2) + f'|{name}|' + symb * int(num_symb / 2))
        match name:
            case 'Login':
                for record in table.select().order_by(table.user_id):
                    print(f'user_id: {record.user_id}')
                    print(f'email: {record.email}')
                    print(f'password: {record.password}')
                    print(f'session_id: {record.session_id}')
                    print(symb * (num_symb + len(name) + 2))

            case 'Email':
                for record in table.select().order_by(table.user_id):
                    print(f'user_id: {record.user_id}')
                    print(f'email_receieve: {record.email_receieve}')
                    print(f'password: {record.password}')
                    print(f'latest_exml_id: {record.latest_exml_id}')
                    print(f'time_stamp: {record.time_stamp}')
                    print(f'is_retrieve: {record.is_retrieve}')
                    print(f'is_comm_report: {record.is_comm_report}')
                    print(symb * (num_symb + len(name) + 2))

            case 'Ownership':
                for record in table.select().order_by(table.user_id):
                    print(f'user_id: {record.user_id}')
                    print(f'xml_id: {record.xml_id}')
                    print(symb * (num_symb + len(name) + 2))            

if __name__ == "__main__":
    # Debug Database
    Database.start()
    #Database.create_tables()
    '''
    login_data = {'password' : 'password',
                            'email' : 'exmaple@gmail.com', 
                            'session_id' : '0 1',
                            'user_id' : 0}
    '''
    #Database.insert('Login', login_data)
    #Database.insert('Ownership', {'user_id':0, 'xml_id':123})
    #data = {'password' :'password', 'email' : 'new2@gmail.com'}
    #Database.update('Login', 0, data)
    #Database.drop_tables()
    #Database.print_table('Login')
    Database.stop()
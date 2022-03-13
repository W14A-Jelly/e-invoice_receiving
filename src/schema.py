import peewee as pw

'''
Define database structure, tables and constraints in database
'''

db = pw.SqliteDatabase('invoice.db', pragmas={'foreign_keys': True,
                                            'ignore_check_contraints': False})

# Constraints definitions
pass_constraint = 'length(password)>=6 AND length(password<=20)'

class Entity(pw.Model):
    class Meta:
        database = db

class Login(Entity):
    user_id = pw.IntegerField(primary_key=True)
    email = pw.TextField(unique=True)
    password = pw.TextField(constraints=[pw.Check(pass_constraint)])
    session_id = pw.TextField()

class Email(Entity):
    user_id = pw.ForeignKeyField(Login)
    email_receive = pw.TextField(unique=True)
    password = pw.TextField(constraints=[pw.Check(pass_constraint)])
    latest_xml_id = pw.TextField(unique=False)
    time_stamp = pw.DateTimeField()
    is_retrieve = pw.BooleanField(default=False)
    is_comm_report = pw.BooleanField(default=False)

class Ownership(Entity):
    user_id = pw.ForeignKeyField(Login)
    xml_id = pw.TextField(unique=True)
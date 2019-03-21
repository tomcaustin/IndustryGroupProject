from psycopg2 import pool


class Database:

    __connection_pool = None

    @staticmethod
    def initialise(**kwargs):
        #database=dbname, host=lclHost, user=logged_in_user, port=postgres_port, password=pwd
        for key, value in kwargs.items():
            print("%s == %s" % (key, value))
        Database.__connection_pool = pool.SimpleConnectionPool(1, 10, **kwargs)

    @staticmethod
    def get_connection():
        return Database.__connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        Database.__connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        Database.__connection_pool.closeall()

class CursorFromConnectionPool:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = Database.get_connection()
        self.cursor = self.conn.cursor()
        return (self.cursor)

    def __exit__(self,exception_type,exception_value,execption_tb):
        if exception_value:   # This is equivalent to `if exception_value is not None`
            self.conn.rollback()
        else:
            self.cursor.close()
            self.conn.commit()
        #Database.connection_pool.putconn(self.connection)
        Database.return_connection(self.conn)

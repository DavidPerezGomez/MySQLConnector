import mysql.connector
from mysql.connector import errorcode


class MysqlConnector:

    _username = 'faeria'
    _password = 'faeria'
    _host = 'localhost'
    _database = 'Faeria'
    _connected = False
    # TODO mover info de conexión a config.py o algo asi...
    _conn = None
    _cursor = None

    def __init__(self, username=None, password=None, host=None, database=None):
        self.set_username(username)
        self.set_password(password)
        self.set_host(host)
        self.set_database(database)

    def __del__(self):
        self.close()

    def is_connected(self):
        return self._connected

    def get_connected_database(self):
        if self.is_connected():
            return self._conn.database
        else:
            return False

    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def set_host(self, host):
        self._host = host

    def set_database(self, database):
        self._database = database

    def connect(self):
        if not self.is_connected():
            error = False
            if self._username is None:
                print("username is not set.")
                error = True
            if self._host is None:
                print("host is not set.")
                error = True
            if self._database is None:
                print("database is not set.")
                error = True
            if not error:
                try:
                    # se intenta entrar al usuario@host con la contraseña
                    self._conn = mysql.connector.connect(user=self._username, password=self._password, host=self._host)
                    # intenta abrir la base de datos
                    self._conn.database = self._database
                    self._cursor = self._conn.cursor(buffered=True)
                    self._connected = True
                    print('Connected to database {}.'.format(self._conn.database))
                except mysql.connector.Error as e:
                    print('Connection could not be established.')
                    print(e)
                    exit(1)
            else:
                self.close()
        else:
            print('Already connected to a database. Please close current connection before opening a new one.')

    def close(self):
        if self.is_connected():
            db = self._conn.database
            self._conn.close()
            self._connected = False
            print('Closed connection with database {}.'.format(db))

    def execute(self):
        pass

    def _create_database():
        try:
            with open(DB_SCRIPT) as f:
                f.readline()
                sql = f.read()
            global _cursor
            _cursor = _conn.cursor()
            _cursor.execute(sql, multi=True)
            _conn.commit()
            # for result in _cursor.execute(sql, multi=True):
            #     if result.with_rows:
            #         print("Rows produced by statement '{}':".format(
            #             result.statement))
            #         print(result.fetchall())
            #     else:
            #         print("Number of rows affected by statement '{}': {}".format(
            #             result.statement, result.rowcount))
        except mysql.connector.Error as e:
            print("Failed creating database: {}".format(e))
            exit(1)


    def executebad(operation, params=(), multi=False):
        if _conn is not None:
            try:
                if not multi:
                    _cursor.execute(operation, params)
                    if _cursor.with_rows:
                        return _cursor.fetchall()
                    else:
                        _conn.commit()
                        return _cursor.rowcount
                else:
                    result = {}
                    i = 0
                    print("foo")
                    for res in _cursor.execute(operation, params, True):
                        if res.with_rows:
                            result[i] = {
                                'statement': res.statement,
                                'lines': res.fetchall()
                            }
                        else:
                            _conn.commit()
                            result[i] = {
                                'statement': res.statement,
                                'affected': res.rowcount
                            }
                        print(res.statement)
                    return result
            except mysql.connector.Error as e:
                sql = operation.replace('%s', '{}').replace('%i', '{}').format(params)
                # print('Error executing query {}'.format(sql))
                print(e)
                exit(1)
        else:
            return False

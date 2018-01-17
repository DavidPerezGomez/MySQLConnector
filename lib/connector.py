import mysql.connector


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
            else:
                self.close()
        else:
            print('Already connected to a database. Please close current connection before opening a new one.')

    def close(self):
        if self.is_connected():
            tmp = self._conn.database
            self._conn.close()
            self._connected = False
            print('Closed connection with database {}.'.format(tmp))
        else:
            print('Connection was not established.')

    def exec(self, operation=''):
        if self.is_connected():
            operations = self._parse_operation(operation)
            results = self._execute(operations)
            return results
        else:
            print('Not connected to any database.')

    @staticmethod
    def _parse_operation(operation):
        if operation.startswith(';'):
            operation = operation[1:]
        if operation.endswith(';'):
            operation = operation[:-1]
        operations = operation.split(';')
        for i in range(0, len(operations)):
            operations[i] = operations[i] + ';'
        return operations

    def _execute(self, operations):
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        results = []
        for op in operations:
            try:
                self._cursor.execute(op, (), False)
                self._conn.commit()
                if self._cursor.with_rows:
                    res = self._cursor.fetchall()
                    results.append(res)
                else:
                    results.append(self._cursor.rowcount)
            except mysql.connector.Error as e:
                print(e)
                results.append(None)
        return results

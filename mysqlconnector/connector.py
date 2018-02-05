import mysql.connector


class MysqlConnector:

    _username = None
    _password = None
    _host = None
    _database = None
    _connected = False
    _conn = None
    _cursor = None

    def __init__(self, username=None, password=None, host=None, database=None):
        self.set_username(username)
        self.set_password(password)
        self.set_host(host)
        self.set_database(database)
        self._conn = None
        self._cursor = None

    def is_connected(self):
        """Returns True if connection with a database has been established, False otherwise."""
        return self._connected

    def get_connected_database(self):
        """Returns the name of the database connected to, False if it's not connected to any database."""
        if self.is_connected():
            return self._conn.database
        else:
            return False

    def set_username(self, username):
        """Sets the username to be connected with"""
        self._username = username

    def set_password(self, password):
        """Sets the password to be connected with"""
        self._password = password

    def set_host(self, host):
        """Sets the host to be connected with"""
        self._host = host

    def set_database(self, database):
        """Sets the username to be connected to"""
        self._database = database

    def connect(self):
        """Connects to the database with the username, host and password given.
        Returns True if successful, False otherwise"""
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
            print('Already connected to a database. Please close current connection before opening a new one.')
        return self.is_connected()

    def close(self):
        """Closes the connection with the database"""
        if self.is_connected():
            tmp = self._conn.database
            self._conn.close()
            self._cursor = None
            self._connected = False
            print('Closed connection with database {}.'.format(tmp))
        else:
            print('Connection had not been established.')

    def exec(self, operation=''):
        """Executes the operation given. Only one operations is accepted.
        If multiple statements are passed, only the first one will be executed.
        Returns a list where each of its elements is one row of the view
        resulting from the sql statement.
        Each one of those row comes in the form of a tuple, with every element
        corresponding to a column.
        In the case of statements where no rows are returned
        (INSERT, UPDATE, DELETE, etc.), it will instead return the number of
        rows affected by the operation."""
        # TODO mencionar lo de que si hay ';' en el propio sql se jode todo
        # TODO testear con nullvalues, etc.
        if self.is_connected():
            operations = self._parse_operations(operation)
            results = self._execute([operations[0]])
            return results[0]
        else:
            print('Not connected to any database.')

    def exec_mult(self, operation=''):
        """Executes the operation or operations given. Multiple operations can
        be executed on a single call. For that, all the statements must come on
        a single string and be separated by ';'. A ';' at the end is not
        required when a single statement is passed.
        Returns a list where each element is the result of one of the sql
        statements.
        Each of the results is a list itself and each of its elements is one
        row of the view resulting from the sql statement.
        Each one of those row comes in the form of a tuple, with every element
        corresponding to a column.
        In the case of statements where no rows are returned
        (INSERT, UPDATE, DELETE, etc.), the list corresponding to the
        result of said statement will instead be the number of rows affected by
        the operation.
        ie.:
        Tables:
        POKEMON(name, type1, type2)
        USER(number, name, age)
        Statement:
        SELECT * FROM pokemon; INSERT INTO user VALUES (4, manuel, 45); SELECT name FROM user;
        Result:
        [[(pikachu, electric, NULL), (bisharp, dark, steel), (castform, normal, NULL)],
        1,
        [(jose,), (pedro,), (marcos,), (manuel,)]]
        """
        if self.is_connected():
            operations = self._parse_operations(operation)
            results = self._execute(operations)
            return results
        else:
            print('Not connected to any database.')

    # @staticmethod
    # def _parse_operations(operation):
    #     """Parses a string containing multiple sql statements separated by ';'
    #     and returns a list containing each of those statements"""
    #     if operation.startswith(';'):
    #         operation = operation[1:]
    #     if operation.endswith(';'):
    #         operation = operation[:-1]
    #     operations = operation.split(';')
    #     for i in range(0, len(operations)):
    #         operations[i] = operations[i] + ';'
    #     return operations

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

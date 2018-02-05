import mysql.connector


class MysqlConnector:

    def __init__(self, username=None, password=None, host=None, database=None):
        self._username = username
        self._password = password
        self._host = host
        self._database = database
        self._connected = False
        self._conn = None
        self._cursor = None

    def is_connected(self):
        """Returns True if connection with a database has been established, False otherwise."""
        return self._connected

    def get_connected_database(self):
        """Returns the name of the database connected to, False if it's not connected to any database."""
        if self.is_connected():
            try:
                return self._conn.database
            except mysql.connector.Error as e:
                print(e)
                print('Please, try closing the current connection and opening a new one.')
        else:
            return None

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
            self._conn.close()
            self._cursor = None
            self._connected = False
            print('Closed connection with database.')
        else:
            print('Connection had not been established.')

    def exec(self, operation='', data=()):
        """Executes the operation given. Only one operations is accepted.
        Returns a list where each of its elements is one row of the view
        resulting from the sql statement.
        Each one of those row comes in the form of a tuple, with every element
        corresponding to a column.
        In the case of statements where no rows are returned
        (INSERT, UPDATE, DELETE, etc.), it will instead return the number of
        rows affected by the operation."""
        if self.is_connected():
            try:
                sql = self._parse_operation(operation)
                self._cursor.execute(sql, data, False)
                if self._cursor.with_rows:
                    result = self._cursor.fetchall()
                else:
                    result = self._cursor.rowcount
                self._conn.commit()
                return result
            except mysql.connector.Error as e:
                print(e)
                return None
        else:
            print('Not connected to any database.')

    def exec_mult(self, operations=''):
        """Executes the operation or operations given. Multiple operations can
        be executed on a single call. For that, all the statements must come on
        a single string and be separated by ';'. A ';' at the end is not
        required.
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
            try:
                results = []
                sql = self._parse_operation(operations)
                for result in self._cursor.execute(sql, (), True):
                    if result.with_rows:
                        results.append(result.fetchall())
                    else:
                        results.append(result.rowcount)
                self._conn.commit()
                return results
            except mysql.connector.Error as e:
                print(e)
                return None
        else:
            print('Not connected to any database.')

    @staticmethod
    def _parse_operation(operation):
        parsed = operation
        while parsed.startswith(';'):
            parsed = parsed[1:]
        while parsed.endswith(';'):
            parsed = parsed[:-1]
        return parsed

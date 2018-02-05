# MySQLConnector
Módulo para trabajar con MySQL en pyhton simplificando el uso de MySQL Connector/Python.
Es necesario tener MySQL Connector/Python:
https://dev.mysql.com/doc/connector-python/en/connector-python-installation-source.html


## Conexión
Primero importar la clase MysqlConnector

    from mysqlconnector.connector import MysqlConnector

e instanciarla

    conn = MysqlConnector(username, password, host, database)

Todos los valores se puede asignar o cambiar más tarde con setter, por lo que pueden ir vacíos en la constructora

    conn.set_username(username)
    conn.set_password(password)
    conn.set_host(host)
    conn.set_database(database)

Cuando todos los valores están asignados, establecer la conexión con

    conn.connect()

Cuando se termina de usar la conexión, cerrarla con

    conn.close()

## Uso
Para ejecutar un solo comando sql

    sql = "INSERT INTO Foo VALUES ('bar')"
    conn.exec(sql)

El resultado de exec depende del tipo de sentencia sql que se ejecute:
* Las sentecias de consulta (SELECT) devuelven una lista de tuplas, donde cada tupla es una fila del resultado
* Las el resto de sentencias (INSERT, UPDATE, DELETE, etc.) devuelven el número de filas que se han visto afectadas por la operación.
Por ejemplo

    sql = "INSERT INTO Foo VALUES ('eggs')"
    res = conn.exec(sql)
    print(res)
    --> 1

    sql = "SELECT * FROM Foo"
    res = conn.exec(sql)
    print(res)
    --> [('bar',), ('eggs',)]

Para ejecutar múltiples comandos de una vez


    sql = "DELETE FROM Foo; INSERT INTO Foo VALUES ('new;bar'), ('scrambled eggs'); SELECT * FROM Foo"
    res = conn.exec_mult(sql)
    print(res)
    --> [2, 2, [('new;bar',), ('scrambled eggs',)]]

Las sentencias deben ir separadas unas de otras por ';'. El resultado es una lista en la que cada elemento corresponde a una de las sentencias y siguen el mismo formato que el resultado de exec()

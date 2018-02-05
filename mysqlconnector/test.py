from mysqlconnector.connector import MysqlConnector

c = MysqlConnector()
c.set_username('test')
c.set_password('test')
c.set_host('localhost')
c.set_database('Test')
c.connect()
sql = ";;;Select * from foo; INSERT INTO foo VALUES ('13');;;"
sql2 = ";;;SELECT * from foo;;"
print(c.exec_mult(sql))
print(c.exec(sql))
c.close()

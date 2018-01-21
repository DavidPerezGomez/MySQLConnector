from lib.connector import MysqlConnector

c = MysqlConnector()
c.set_username('faeria')
c.set_password('faeria')
c.set_host('localhost')
c.set_database('Faeria')
c.connect()
sql = ";Select * from card; INSERT INTO deck VALUES ('deck10'); SELECT * from deck;"
print(c.exec(sql))
c.close()

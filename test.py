from lib.connector import MysqlConnector

c = MysqlConnector()
c.set_username('faeria')
c.set_password('faeria')
c.set_host('localhost')
c.set_database('Faeria')
c.connect()
sql = ";insert into deck values ('deck9'); SELECT * from deck;"
c.exec(sql)
c.close()

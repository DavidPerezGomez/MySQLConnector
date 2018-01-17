from lib.connector import MysqlConnector

c = MysqlConnector()
c.connect()
c.close()

c.set_username('faeria')
c.connect()
c.close()

c.set_password('faeria')
c.connect()
c.close()

c.set_host('localhost')
c.connect()
c.close()

c.set_database('Faeria')
c.connect()
c.close()

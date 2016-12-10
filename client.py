from suds.client import Client

c = Client('http://localhost:8000/lalaland?wsdl')
c.options.cache.clear()
print(c)
print(c.service.say_hello('punk', 5))
print(c.service.consulta_db())
print(c.service.insert_db('2016-12-12', '18:00', 'Barcelona', '17.12', '57', '1001.23',))

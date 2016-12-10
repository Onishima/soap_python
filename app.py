from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import sqlite3
import collections


class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield u'Hello, %s' % name

class Consulta_DB(ServiceBase):
	@rpc(_returns=Iterable(Unicode)) #decorator
	def consulta_db(ctx):
		conn = sqlite3.connect('meteofib.db')
		print "Opened database successfully";
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM meteofib_table")
		rv = cursor.fetchall()
		conn.close()
		row_list = []
		result = ""
		for row in rv:
			result = "Fecha: "
			result += row[0]
			result += " Hora: "
			result += row[1]
			result += " Ciudad: "
			result += row[2]
			result += " Temperatura: "
			result += row[3]
			result += " Humedad: "
			result += row[4]
			result += " P_atmos: "
			result += row[5]
			yield(result)

class Insert_DB(ServiceBase):
	@rpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode) #decorator
	def insert_db(ctx, fecha, hora, ciudad, temperatura, humedad, p_atmos):

		query = "INSERT INTO meteofib_table (fecha, hora, ciudad, temperatura, humedad, p_atmos) VALUES ('"
		query += fecha
		query += "', '"
		query += hora
		query += "', '"
		query += ciudad
		query += "', '"
		query += temperatura
		query += "', '"
		query += humedad
		query += "', '"		
		query += p_atmos
		query += "')"

		conn = sqlite3.connect('meteofib.db')
		print "Opened database successfully";
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		conn.close()


application = Application([HelloWorldService, Consulta_DB, Insert_DB], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
	import logging

	from wsgiref.simple_server import make_server

	logging.basicConfig(level=logging.DEBUG)
	logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

	logging.info("listening to http://127.0.0.1:8000")
	logging.info("wsdl is at: http://localhost:8000/lalaland?wsdl")

	server = make_server('127.0.0.1', 8000, wsgi_application)
	server.serve_forever()

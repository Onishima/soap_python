from flask import Flask
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable
import sqlite3
import collections

app = Flask(__name__)
spyne = Spyne(app)

class SomeSoapService(spyne.Service):
	__service_url_path__ = '/soap/someservice'
	__in_protocol__ = Soap11(validator='lxml')
	__out_protocol__ = Soap11()

	@spyne.srpc(Unicode, Integer, _returns=Iterable(Unicode))
	def echo(str, cnt):
		for i in range(cnt):
			yield str

	@spyne.srpc(_returns=Iterable(Unicode)) #decorator
	def consulta_db():
		conn = sqlite3.connect('meteofib.db')
		print "Opened database successfully";
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM meteofib_table")
		rv = cursor.fetchall()
		cursor.close()
		row_list = []
		for row in rv:
			d = collections.OrderedDict()
			d['Fecha'] = row[0]
			d['Hora'] = row[1]
			d['Ciudad'] = row[2]
			d['Temperatura'] = row[3]
			d['Humedad'] = row[4]
			d['P_atmos'] = row[5]
			row_list.append(d)
		yield(str(rv))

if __name__ == '__main__':
	app.run(host = '127.0.0.1')


from flask import Flask, jsonify, session, redirect, url_for, escape, request, render_template
import requests, json
from suds.client import Client
from forms import InsertForm

app = Flask(__name__)

headers = {'Content-Type': 'application/soap+xml; charset="UTF-8"'}
app.secret_key = 'development key'

@app.route('/')
def home():
	
	#print(c)
	#print(c.service.say_hello('punk', 5))
	#print(c.service.consulta_db())
	#print(c.service.insert_db('2016-12-12', '18:00', 'local3', '17.12', '57', '1001.23',))
	return render_template('index.html')


@app.route('/index.html')
def index():
	return render_template('index.html')

@app.route('/tiempo.html')
def tiempo():
	try:
		header = ['Fecha', 'Hora', 'Ciudad', 'Temperatura', 'Humedad', 'Presion Atm.']
		c = Client('http://localhost:9000/lalaland?wsdl', headers=headers)
		c.options.cache.clear()	
		data=[]
		fecha = []
		hora = []
		ciudad = []
		temperatura = []
		humedad = []
		p_atmos = []
		table = []
		data = c.service.consulta_db()
		datos = data[0]
		for row in datos:
			mycollapsedstring = ' '.join(row.split())
			aux = mycollapsedstring.split(' ')
			fecha.append(aux[0])
			hora.append(aux[1])
			ciudad.append(aux[2])
			temperatura.append(aux[3])
			humedad.append(aux[4])
			p_atmos.append(aux[5])
			table.append(aux)

		return render_template('tiempo.html', header=header, table=table) 

	except:
		return render_template('error.html',causa="Error de Conexion.") 

@app.route('/insert.html', methods=['GET', 'POST'])
def insert():
	form = InsertForm()
	
	try:
		c = Client('http://localhost:9000/lalaland?wsdl', headers=headers)
		c.options.cache.clear()
	except:
		return render_template('error.html', causa="No se puede enviar datos a la Estacion.")	

	if request.method == 'POST':
		fecha = form.fecha.data
		hora = form.hora.data
		ciudad = form.ciudad.data
		temperatura = form.temperatura.data
		humedad = form.humedad.data
		p_atmos = form.p_atmos.data
		data = c.service.insert_db(fecha, hora, ciudad, temperatura, humedad, p_atmos,)
		datos = data[0]
		if str(datos) == '[OK]':
			return render_template('formulario.html', success=True)
		else:			
			return render_template('error.html',causa="Error de en la entrada.")

	elif request.method == 'GET':
		return render_template('formulario.html', form=form)


@app.route('/ciudad.html', methods=['GET', 'POST'])
def ciudad():

	if request.method == 'POST':
		try:
			header = ['Fecha', 'Hora', 'Ciudad', 'Temperatura', 'Humedad', 'Presion Atm.']
			c = Client('http://localhost:9000/lalaland?wsdl', headers=headers)
			c.options.cache.clear()	
			data=[]
			fecha = []
			hora = []
			ciudad = []
			temperatura = []
			humedad = []
			p_atmos = []
			table = []
			ciutat = request.form.get("ciudad","")
			data = c.service.consulta_ciudad(ciutat)
			datos = data[0]
			if str(datos) == '[-1]':
				return render_template('error.html',causa="Error de en el nombre de la Ciudad.")
			for row in datos:
				mycollapsedstring = ' '.join(row.split())
				aux = mycollapsedstring.split(' ')
				fecha.append(aux[0])
				hora.append(aux[1])
				ciudad.append(aux[2])
				temperatura.append(aux[3])
				humedad.append(aux[4])
				p_atmos.append(aux[5])
				table.append(aux)

			return render_template('ciudad.html', header=header, table=table, success=False ) 

		

		except:
			return render_template('error.html',causa="Error.")
			
	elif request.method == 'GET':
		return render_template('ciudad.html', success=True)


if __name__ == "__main__":
    app.run(port=5001)
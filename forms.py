from flask_wtf import FlaskForm as Form
from wtforms import TextField, SubmitField, validators, TextAreaField, BooleanField

class InsertForm(Form):
  fecha = TextField("fecha")
  hora = TextField("hora")
  ciudad = TextField("ciudad")
  temperatura = TextField("temperatura")
  humedad = TextField("humedad")
  p_atmos = TextField("p_atmos")
  submit = SubmitField("Envia")




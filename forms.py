from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PersonaForm(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired()])
    contrasenia = StringField('Contraseña', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    departamento = StringField('Departamento(Comercial o GTR)', validators=[DataRequired()])
    enviar = SubmitField('Enviar')

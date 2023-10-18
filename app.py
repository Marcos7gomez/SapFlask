import re

import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, url_for, flash, session
from flask_migrate import Migrate
# from werkzeug.security import check_password_hash, generate_password_hash
#from sqlalchemy.testing.pickleable import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

# Configuración de la bd
USER_DB = 'postgres'
PASS_BD = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_BD}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
conn = psycopg2.connect(dbname=NAME_DB, user=USER_DB, password=PASS_BD, host=URL_DB)
# Inicialización del objeto db de sqlalchemy
# db = SQLAlchemy(app)

db.init_app(app)
# configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

# Configuración de flask-wtf
app.config['SECRET_KEY'] = 'llave_secreta'


@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home2.html', usuario=session['usuario'])
    return redirect(url_for('login'))


@app.route('/list')
def inicio():
    # Listado de personas
    personas = Persona.query.all()
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)


@app.route('/ver/<int:id>')
def ver_detalle(id):
    # Recuperamos la persona según id proporcionado
    # persona = Persona.query.get(id)
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona=persona)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    persona = Persona()
    personaForm = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            app.logger.debug(f'Persona a insertar: {persona}')
            # Insertammos el nuevo registro en la base de datos
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('agregar.html', forma=personaForm)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #Verifica si usuario y contrasenia existen
    if request.method == 'POST' and 'usuario' in request.form and 'contrasenia' in request.form:
        usuario = request.form['usuario']
        contrasenia = request.form['contrasenia']
        print(contrasenia)
        # Verifica si la cuneta existe en la bd
        cursor.execute('SELECT * FROM persona WHERE usuario = %s', (usuario,))
        # Obtiene un registro y da un resultado
        cuenta = cursor.fetchone()
        if cuenta:
            password_rs = cuenta['contrasenia']
            print(password_rs)
            #Si la cuenta existe en usuario de la bd
            if check_password_hash(password_rs, contrasenia):
                session['loggedin'] = True
                session['id'] = cuenta['id']
                session['usuario'] = cuenta['usuario']
                print('Sesión exitosa')
                return redirect(url_for('home'))
            else:
                flash('¡La cuenta ingresada no existe!')
        else:
            flash('¡La cuenta ingresada no existe!')
        # return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'usuario' in request.form and 'contrasenia' in request.form and 'email' \
            in request.form:
        # Create variables for easy access
        usuario = request.form['usuario']
        departamento = request.form['departamento']
        contrasenia = request.form['contrasenia']
        email = request.form['email']

        _hashed_password = generate_password_hash(contrasenia)

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM persona WHERE usuario = %s', (usuario,))
        cuenta = cursor.fetchone()
        print(cuenta)
        # If account exists show error and validation checks
        if cuenta:
            flash('¡Esta cuenta ya existe!!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Dirección de email inválida!')
        elif not re.match(r'[A-Za-z0-9]+', usuario):
            flash('EL usuario debe contener sólo palabras y números!')
        elif not contrasenia or not contrasenia or not email:
            flash('¡Por favor rellena el formulario!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO persona (usuario, departamento, contrasenia, email) VALUES (%s,%s,%s,%s)",
                           (usuario, departamento, _hashed_password, email))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')

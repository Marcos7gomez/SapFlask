from datetime import datetime

from flask import session

from app import db



class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(250))
    contrasenia = db.Column(db.String(250))
    email = db.Column(db.String(250))
    departamento = db.Column(db.String(250))

    def __str__(self):
        return (
            f'Id: {self.id},'
            f'Usuario: {self.usuario},'
            f'Contrasenia: {self.contrasenia},'
            f'Email: {self.email},'
            f'Departamento: {self.departamento},'
        )


# Parte de fran

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(250), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(20), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    creador = db.Column(db.String(100), nullable=True)
    comentarios = db.relationship('Comentario', backref='ticket', lazy=True)

    def __str__(self):
        return (
            f'Id: {self.id},'
            f'Titulo: {self.titulo},'
            f'Descripcion: {self.descripcion},'
            f'Estado: {self.estado},'
            f'Fecha_creacion: {self.fecha_creacion},'
            f'Creador: {self.creador},'
            f'Comentarios: {self.comentarios},'
        )

    def agregar_comentario(self, contenido, creador=None):
        nuevo_comentario = Comentario(contenido=contenido, ticket_id=self.id, creador=['usuario'])
        db.session.add(nuevo_comentario)
        db.session.commit()


class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(255), nullable=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    creador = db.Column(db.String(255), nullable=True)

    def asignar_creador(self):
        if 'usuario' in session:
            self.creador = session['usuario']

    def agregar_comentario(self, contenido, creador):
        nuevo_comentario = Comentario(contenido=contenido, ticket_id=self.id, creador=None)
        db.session.add(nuevo_comentario)
        db.session.commit()
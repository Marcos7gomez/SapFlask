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

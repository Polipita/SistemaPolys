from src.extensions import db

class Usuario(db.Model):
    __tablename__='usuarios'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120),nullable=False ,unique=True)
    password = db.Column(db.String(255))
    rol = db.Column(db.String(20), nullable=False, default='EMPLEADO')

    empresas_id = db.Column(db.Integer,db.ForeignKey('empresas.id'),nullable=False)
from src.extensions import db

class Empresa(db.Model):
    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100),nullable=False)
    ruc = db.Column(db.String(11),nullable=False,unique=True)
    estado = db.Column(db.Boolean,default=True)

    usuarios = db.relationship('Usuario', backref='empresa', lazy=True)
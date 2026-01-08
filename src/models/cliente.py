from src.extensions import db 

class Cliente(db.Model):
    __tablename__='clientes'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(120),nullable =False)
    telefono = db.Column(db.String(11),nullable = False)
    email = db.Column(db.String(120))

    empresas_id = db.Column(db.Integer,db.ForeignKey('empresas.id'),nullable=False)

    mascotas = db.relationship('Mascota', backref='cliente', lazy=True)
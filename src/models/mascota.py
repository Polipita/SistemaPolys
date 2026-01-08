from src.extensions import db

class Mascota(db.Model):
    __tablename__ = "mascotas"
    
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50),nullable = False)
    raza = db.Column(db.String(30))
    fecha_nacimiento = db.Column(db.Date)

    clientes_id = db.Column(db.Integer,db.ForeignKey('clientes.id'),nullable=False)
    empresas_id = db.Column(db.Integer,db.ForeignKey('empresas.id'),nullable=False)
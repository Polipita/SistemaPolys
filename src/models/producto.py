from src.extensions import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False, default=0.0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    
    #si tiene pistola lectora
    codigo_barras = db.Column(db.String(50), nullable=True)
    tipo = db.Column(db.String(20), nullable=False, default='PRODUCTO')

    empresas_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
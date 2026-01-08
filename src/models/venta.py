from datetime import datetime
from src.extensions import db

class Venta(db.Model):
    __tablename__ = 'ventas'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now)
    total = db.Column(db.Float, default=0.0)
    
    clientes_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    usuarios_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    empresas_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)

    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)
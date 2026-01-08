from src.extensions import db

class DetalleVenta(db.Model):
    __tablename__ = 'detalles_ventas'

    id = db.Column(db.Integer, primary_key=True)
    
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    ventas_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    productos_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
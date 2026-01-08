from datetime import datetime
from src.extensions import db

class Historia(db.Model):
    __tablename__ = 'historias'

    id = db.Column(db.Integer, primary_key=True)
    motivo = db.Column(db.String(250))
    diagnostico = db.Column(db.String(250))
    tratamiento = db.Column(db.String(250))
    
    fecha = db.Column(db.DateTime, default=datetime.now)


    mascotas_id = db.Column(db.Integer,db.ForeignKey('mascotas.id'),nullable=False)
    usuarios_id = db.Column(db.Integer,db.ForeignKey('usuarios.id'),nullable=False)
    empresas_id = db.Column(db.Integer,db.ForeignKey('empresas.id'),nullable=False)
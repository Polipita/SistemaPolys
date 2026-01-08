from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.extensions import db
from src.models.mascota import Mascota
from src.models.cliente import Cliente

mascota_bp = Blueprint('mascota', __name__, url_prefix='/api/mascotas')

@mascota_bp.route('/', methods=['POST'])
@jwt_required()  
def crear_mascota():
    try:
        claims = get_jwt() 
        mi_empresa_id = claims['empresa_id'] 

        data = request.get_json()

        if not data.get('clientes_id'):
            return jsonify({'error': 'Debes indicar el ID del dueño (clientes_id)'}), 400

        nueva_mascota = Mascota(
            nombre=data['nombre'],
            raza=data.get('raza'),
            fecha_nacimiento=None, 
            clientes_id=data['clientes_id'],
            empresas_id=mi_empresa_id
        )

        db.session.add(nueva_mascota)
        db.session.commit()

        return jsonify({'mensaje': 'Mascota registrada', 'id': nueva_mascota.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@mascota_bp.route('/', methods=['GET'])
@jwt_required()
def listar_mis_mascotas():
    claims = get_jwt()
    mi_empresa_id = claims['empresa_id']

    mascotas = Mascota.query.filter_by(empresas_id=mi_empresa_id).all()

    resultado = []
    for m in mascotas:
        resultado.append({
            'id': m.id,
            'nombre': m.nombre,
            'raza': m.raza,
            'dueño_id': m.clientes_id,
            'dueño_nombre': m.cliente.nombre, 
            'dueño_telefono': m.cliente.telefono
        })

    return jsonify(resultado), 200


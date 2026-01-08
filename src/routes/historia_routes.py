from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.extensions import db
from src.models.historia import Historia
from src.models.mascota import Mascota


historia_bp = Blueprint('histroia', __name__, url_prefix='/api/historias')

@historia_bp.route('/',methods=['POST'])
@jwt_required()
def crear_historia():
    try:
        usuario_actual_id = get_jwt_identity()

        claims = get_jwt()
        mi_empresa_id = claims['empresa_id']

        data = request.get_json()

        if not data.get('mascotas_id'):
            return jsonify({'error': 'Falta el ID de la mascota (mascotas_id)'}), 400
        
        nueva_historia = Historia(
            motivo=data['motivo'],
            diagnostico=data.get('diagnostico'),
            tratamiento=data.get('tratamiento'),
            mascotas_id=data['mascotas_id'],
            usuarios_id=usuario_actual_id,
            empresas_id=mi_empresa_id
        )
        db.session.add(nueva_historia)
        db.session.commit()

        return jsonify({
            'mensaje': 'Consulta guardad con exito',
            'id': nueva_historia.id,
            'doctor_id': usuario_actual_id
        })
    except Exception as e :
        return jsonify({'error': str(e)}),500
    
@historia_bp.route("/<int:id_de_mascota>", methods=['GET'])
@jwt_required()
def buscar_historia(id_de_mascota):
    try:
        claims = get_jwt()
        mi_empresa_id = claims['empresa_id']

        historias = Historia.query.filter_by(
            mascotas_id = id_de_mascota,
            empresas_id=mi_empresa_id).all()

        resultado = []

        for consulta in historias:
            fila = {
                'id_historia':consulta.id,
                'fecha':consulta.fecha.strftime('%Y-%m-%d %H:%M'),
                'motivo': consulta.motivo,
                'diagnostico':consulta.diagnostico,
                'tratamiento':consulta.tratamiento,
                'doctor_id':consulta.usuarios_id
            }
            resultado.append(fila)

        return jsonify(resultado),200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    








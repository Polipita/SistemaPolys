from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.extensions import db
from src.models.mascota import Mascota
from src.models.cliente import Cliente

mascota_bp = Blueprint('mascota', __name__, url_prefix='/api/mascotas')

# --- RUTA 1: CREAR UNA NUEVA MASCOTA (POST) ---
@mascota_bp.route('/', methods=['POST'])
@jwt_required()  # <--- ¡EL GUARDIÁN! Sin token no pasas
def crear_mascota():
    try:
        # 1. Obtenemos los datos del "Brazalete" (Token)
        claims = get_jwt() # Leemos los datos extra que guardamos en el login
        mi_empresa_id = claims['empresa_id'] # ¡Aquí está la magia SaaS!

        # 2. Recibimos los datos del formulario (JSON)
        data = request.get_json()

        # (Validación rápida: Verificar que envíen cliente_id)
        if not data.get('clientes_id'):
            return jsonify({'error': 'Debes indicar el ID del dueño (clientes_id)'}), 400

        # 3. Creamos la mascota asignándole la empresa del token automáticmente
        nueva_mascota = Mascota(
            nombre=data['nombre'],
            raza=data.get('raza'), # .get() por si no lo envían (es opcional)
            fecha_nacimiento=None, # Lo dejamos null por ahora para facilitar la prueba
            clientes_id=data['clientes_id'],
            empresas_id=mi_empresa_id # <--- SE ASIGNA SOLO, NO LO PIDE EL USUARIO
        )

        db.session.add(nueva_mascota)
        db.session.commit()

        return jsonify({'mensaje': 'Mascota registrada', 'id': nueva_mascota.id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- RUTA 2: LISTAR SOLO MIS MASCOTAS (GET) ---
@mascota_bp.route('/', methods=['GET'])
@jwt_required()
def listar_mis_mascotas():
    # 1. Leemos de qué empresa es el usuario que pregunta
    claims = get_jwt()
    mi_empresa_id = claims['empresa_id']

    # 2. FILTRO SAAS: "Select * from mascotas WHERE empresa_id = MI_EMPRESA"
    mascotas = Mascota.query.filter_by(empresas_id=mi_empresa_id).all()

    # 3. Convertimos los objetos a JSON (Serialización manual por ahora)
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


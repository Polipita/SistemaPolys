from flask import Blueprint, request, jsonify
from src.extensions import db
from src.models.empresa import Empresa
from src.models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register-company', methods=['POST'])
def register_company():
    # 2. Recibimos los datos que nos envía el usuario (JSON)
    data = request.get_json()

    # (Aquí deberías validar que envíen nombre, email, etc. Lo saltamos por ahora)

    try:
        # 3. LÓGICA: Primero creamos la empresa
        nueva_empresa = Empresa(
            nombre=data['nombre_empresa'],
            ruc=data['ruc']
        )
        
        # Guardamos la empresa primero para que genere un ID
        db.session.add(nueva_empresa)
        db.session.flush() # flush() genera el ID sin cerrar la transacción todavía

        # 4. LÓGICA: Creamos al dueño (Usuario Admin)
        # Encriptamos la contraseña por seguridad
        password_encriptada = generate_password_hash(data['password'])
        
        nuevo_usuario = Usuario(
            email=data['email'],
            password=password_encriptada,
            empresas_id=nueva_empresa.id, # ¡Aquí usamos el ID de la empresa recién creada!
            rol="ADMIN"
        )

        db.session.add(nuevo_usuario)

        # 5. Confirmamos todo en la base de datos
        db.session.commit()

        return jsonify({'message': 'Empresa y Usuario creados exitosamente'}), 201

    except Exception as e:
        db.session.rollback() # Si algo falla, deshace todo (no crea ni empresa ni usuario)
        return jsonify({'error': str(e)}), 500
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')

    # 1. Buscar al usuario por email
    usuario = Usuario.query.filter_by(email=email).first()

    # 2. Verificar: ¿Existe el usuario? ¿La contraseña coincide con el hash?
    if not usuario or not check_password_hash(usuario.password, password):
        return jsonify({'error': 'Credenciales incorrectas'}), 401

    # 3. Si pasa, CREAMOS EL TOKEN (El brazalete)
    # identity: Generalmente es el ID del usuario
    # additional_claims: Guardamos datos extra útiles para no consultar la BD a cada rato
    access_token = create_access_token(
        identity=str(usuario.id),
        additional_claims={
            'empresa_id': usuario.empresas_id,
            'rol': usuario.rol
        }
    )

    return jsonify({
        'mensaje': 'Login exitoso',
        'token': access_token,
        'usuario': usuario.email,
        'rol': usuario.rol
    }), 200
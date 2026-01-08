from flask import Blueprint, request, jsonify
from src.extensions import db
from src.models.empresa import Empresa
from src.models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register-company', methods=['POST'])
def register_company():
    data = request.get_json()

    try:
        nueva_empresa = Empresa(
            nombre=data['nombre_empresa'],
            ruc=data['ruc']
        )
        
        
        db.session.add(nueva_empresa)
        db.session.flush()

        password_encriptada = generate_password_hash(data['password'])
        
        nuevo_usuario = Usuario(
            email=data['email'],
            password=password_encriptada,
            empresas_id=nueva_empresa.id, 
            rol="ADMIN"
        )

        db.session.add(nuevo_usuario)

        db.session.commit()

        return jsonify({'message': 'Empresa y Usuario creados exitosamente'}), 201

    except Exception as e:
        db.session.rollback() 
        return jsonify({'error': str(e)}), 500
    
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not check_password_hash(usuario.password, password):
        return jsonify({'error': 'Credenciales incorrectas'}), 401

   
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
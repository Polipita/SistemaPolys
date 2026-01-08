from flask import Blueprint,request,jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.extensions import db
from src.models.producto import Producto

producto_bp = Blueprint('producto',__name__,url_prefix='/api/productos')

@producto_bp.route('/',methods=['POST'])
@jwt_required()
def crear_productos():
    try:
        claims = get_jwt()
        mi_empresa_id = claims['empresa_id']
        data = request.get_json()

        nuevo_producto = Producto(
            nombre = data['nombre'],
            precio = data['precio'],
            stock = data['stock'],
            codigo_barras = data.get('codigo_barras'),
            empresas_id =mi_empresa_id,
            tipo=data.get('tipo', 'PRODUCTO')
        )
        db.session.add(nuevo_producto)
        db.session.commit()

        return jsonify({'mensaje':'Producto creado',
                        'id':nuevo_producto.id}),201
    
    except Exception as e :
        return jsonify({'error':e}),500
    
@producto_bp.route('/',methods=['GET'])
@jwt_required()
def listar_productos():
    claims = get_jwt()
    mi_empresa_id = claims['empresa_id']

    productos = Producto.query.filter_by(empresas_id=mi_empresa_id).all()

    resultado =[]

    for producto in productos:
        resultado.append({
            'id':producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'stock': producto.stock
        })
    
    return jsonify(resultado),200
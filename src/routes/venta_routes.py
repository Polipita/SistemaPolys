from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from src.extensions import db
from src.models.venta import Venta
from src.models.detalle_venta import DetalleVenta
from src.models.producto import Producto
from sqlalchemy import func
from datetime import datetime 

venta_bp = Blueprint('venta', __name__, url_prefix='/api/ventas')

@venta_bp.route('/', methods=['POST'])
@jwt_required()
def crear_venta():
    try:
        usuario_id = get_jwt_identity()
        claims = get_jwt()
        empresa_id = claims['empresa_id']

        data = request.get_json()
        cliente_id = data.get('cliente_id')
        items = data.get('items')

        if not items:
            return jsonify({'error': 'No hay items en la venta'}), 400

        nueva_venta = Venta(
            fecha=None, 
            total=0.0,
            clientes_id=cliente_id,
            usuarios_id=usuario_id,
            empresas_id=empresa_id
        )
        
        db.session.add(nueva_venta)
        db.session.flush()

        total_acumulado = 0.0

        for item in items:
            cantidad = item['cantidad']
            prod_id = item['id']

            producto_db = Producto.query.filter_by(id=prod_id, empresas_id=empresa_id).first()

            if not producto_db:
                raise Exception(f"Producto ID {prod_id} no encontrado o no autorizado")

            if producto_db.tipo == 'PRODUCTO':
                if producto_db.stock < cantidad:
                    raise Exception(f"Stock insuficiente para {producto_db.nombre}. Hay {producto_db.stock}")
                
                producto_db.stock -= cantidad

            precio_actual = producto_db.precio
            subtotal = precio_actual * cantidad
            total_acumulado += subtotal

            nuevo_detalle = DetalleVenta(
                cantidad=cantidad,
                precio_unitario=precio_actual,
                subtotal=subtotal,
                ventas_id=nueva_venta.id,
                productos_id=producto_db.id
            )
            db.session.add(nuevo_detalle)

        nueva_venta.total = total_acumulado

        db.session.commit()

        return jsonify({
            'mensaje': 'Venta registrada correctamente',
            'id_venta': nueva_venta.id,
            'total': total_acumulado
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@venta_bp.route('/reporte', methods=['GET'])
@jwt_required()
def reporte_ventas():
    try:
        claims = get_jwt()
        mi_empresa_id = claims['empresa_id']

        fecha_inicio_str = request.args.get('inicio')
        fecha_fin_str = request.args.get('fin')

        if not fecha_inicio_str or not fecha_fin_str:
            return jsonify({'error': 'Debes enviar fecha inicio y fin (YYYY-MM-DD)'}), 400

        inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        fin = datetime.strptime(fecha_fin_str + " 23:59:59", '%Y-%m-%d %H:%M:%S')

        # 2. LA CONSULTA MAESTRA (SQLAlchemy)
        # Queremos: Nombre, Tipo, Suma de Cantidad, Suma de Dinero
        resultados = db.session.query(
            Producto.nombre,
            Producto.tipo,
            func.sum(DetalleVenta.cantidad).label('total_vendidos'),
            func.sum(DetalleVenta.subtotal).label('dinero_generado')
        ).join(DetalleVenta, Producto.id == DetalleVenta.productos_id) \
         .join(Venta, DetalleVenta.ventas_id == Venta.id) \
         .filter(Venta.empresas_id == mi_empresa_id) \
         .filter(Venta.fecha.between(inicio, fin)) \
         .group_by(Producto.id, Producto.nombre, Producto.tipo) \
         .all()

        
        reporte = []
        total_general = 0

        for fila in resultados:
            dinero = float(fila.dinero_generado)
            total_general += dinero

            reporte.append({
                'producto': fila.nombre,
                'tipo': fila.tipo, 
                'cantidad_vendida': int(fila.total_vendidos),
                'ingresos': dinero
            })

        return jsonify({
            'periodo': {'inicio': fecha_inicio_str, 'fin': fecha_fin_str},
            'total_periodo': total_general,
            'detalles': reporte
        }), 200

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
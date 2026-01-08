from flask import Flask
from src.extensions import db, migrate,jwt
from config import Config
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    
    from src.models import empresa, usuario, cliente, mascota, historia, producto, venta,detalle_venta

    
    from src.routes.auth import auth_bp
    from src.routes.mascota import mascota_bp
    from src.routes.historia_routes import historia_bp
    from src.routes.producto_routes import producto_bp
    from src.routes.venta_routes import venta_bp

    # registrar en la app para la ruta
    app.register_blueprint(auth_bp)
    app.register_blueprint(mascota_bp)
    app.register_blueprint(historia_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(venta_bp)


    return app
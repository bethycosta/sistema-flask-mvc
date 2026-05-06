from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import render_template

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
    app.config['JWT_SECRET_KEY'] = 'segredo-super'

    @app.route("/")
    def home():
        return render_template("index.html")

    db.init_app(app)
    jwt.init_app(app)

    from app.controllers.user_controller import user_bp
    from app.controllers.product_controller import product_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)

    with app.app_context():
        db.create_all()

    return app
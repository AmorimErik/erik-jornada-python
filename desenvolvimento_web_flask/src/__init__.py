from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import DATABASE_URI

database = SQLAlchemy()


def create_app():
    app = Flask(__name__)  # Criando e configurando uma instância do Flask
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "d718df7d5300f2ec0a950cd9b804445b"

    database.init_app(app)  # Conectando o banco de dados

    from src.routes import main_bp

    app.register_blueprint(main_bp)

    with app.app_context():
        database.create_all()

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "img.db"


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()

    from .views import views
    from .camera_routes import camera

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(camera, url_prefix='/camera')

    return app

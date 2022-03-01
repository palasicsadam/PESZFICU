import imp
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ASDASDASFDASD"
    
    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app
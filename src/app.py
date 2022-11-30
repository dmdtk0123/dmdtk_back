from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder="templates")
    CORS(app, resources={r"*": {"origins": "*"}})

    from views import content_input_views as ci_views

    app.register_blueprint(ci_views.bp)

    return app

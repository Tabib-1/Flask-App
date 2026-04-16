import os
from flask import Flask
from .db import init_db
from .routes import bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['DATABASE'] = os.path.join(app.instance_path, 'users.db')

    os.makedirs(app.instance_path, exist_ok=True)

    app.register_blueprint(bp)

    with app.app_context():
        init_db()

    return app
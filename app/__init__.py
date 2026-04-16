import os
from datetime import timedelta

from flask import Flask

from .db import init_db, close_db
from .routes import bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key-change-me"),
        DATABASE=os.path.join(app.instance_path, "users.db"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
    )

    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    app.teardown_appcontext(close_db)
    app.register_blueprint(bp)

    @app.context_processor
    def inject_current_user():
        from flask import g
        return {"current_user": getattr(g, "user", None)}

    with app.app_context():
        init_db()

    return app
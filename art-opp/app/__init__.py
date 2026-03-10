from __future__ import annotations

from flask import Flask


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATA_FILE="data/opportunities.json",
    )

    if test_config:
        app.config.update(test_config)

    from . import routes

    routes.init_app(app)
    return app

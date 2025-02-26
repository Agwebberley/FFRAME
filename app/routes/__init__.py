from flask import Blueprint
from app.routes.test_log import test_log_bp

def register_blueprints(app):
    app.register_blueprint(test_log_bp)

from flask import Flask
from flask_graphql import GraphQLView
from app.models import *
from app.extensions import db, migrate
from app.extensions.logging import setup_logging
from app.routes import register_blueprints
from .graphql.schema import schema


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register all Blueprints
    register_blueprints(app)

    # Setup Logging
    setup_logging(app)

    # GraphQL endpoint
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True  # Enable GraphiQL UI
        )
    )

    return app

from app.extensions import db


def get_all_models():
    """Retrieve all SQLAlchemy models dynamically."""
    models = {}
    for model_class in db.Model.registry._class_registry.values():
        if hasattr(model_class, '__tablename__'):  # Ensure it's a real SQLAlchemy model
            models[model_class.__name__] = model_class
    return models

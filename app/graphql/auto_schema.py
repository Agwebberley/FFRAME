import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

# Cache dictionary to store generated types
_generated_types = {}


def generate_graphql_type(model):
    type_name = f"{model.__name__}Type"
    if type_name in _generated_types:
        return _generated_types[type_name]

    _model = model  # Capture the model to avoid scope issues

    class Meta:
        model = _model
        interfaces = (graphene.relay.Node,)

    generated_type = type(type_name, (SQLAlchemyObjectType,), {"Meta": Meta})
    _generated_types[type_name] = generated_type
    return generated_type

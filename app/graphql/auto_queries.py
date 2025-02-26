# app/graphql/auto_queries.py
import graphene
from app.graphql.utils import get_all_models
from app.graphql.auto_schema import generate_graphql_type


def generate_queries():
    query_fields = {}
    models = get_all_models()
    for model_name, model_class in models.items():
        gql_type = generate_graphql_type(model_class)
        field_name = f"all_{model_name.lower()}s"

        # We use a lambda that captures the current model_class as a default argument.
        resolver = lambda self, info, model=model_class: model.query.all()

        # Create a Graphene field and attach the resolver
        query_fields[field_name] = graphene.List(gql_type, resolver=resolver)

    # Dynamically create the Query class
    return type("Query", (graphene.ObjectType,), query_fields)

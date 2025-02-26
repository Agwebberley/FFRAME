import graphene
from app.extensions import db
from app.graphql.utils import get_all_models
from app.graphql.auto_schema import generate_graphql_type
from app.services.registry import get_service_for_model
from flask import current_app


def make_create_mutation(model_name, model_class, gql_type, InputType):
    mutation_cls = None  # Placeholder for the generated mutation class

    def mutate(self, info, input_data):
        current_app.logger.debug(f"Attempting to create {model_name} with data: {input_data}")
        service = get_service_for_model(model_name)
        if service is not None:
            if not hasattr(service, "create"):
                current_app.logger.error(f"Service for model {model_name} does not implement 'create'")
                raise Exception(f"Service for model {model_name} does not implement 'create'")
            current_app.logger.debug(f"Using service for creating {model_name}")
            new_obj = service.create(input_data, info.context)
        else:
            # This block should only be reached if no service is defined for this model.
            current_app.logger.warning(f"No service found for model {model_name}; using fallback auto-generated create.")
            new_obj = model_class(**input_data)
            db.session.add(new_obj)
            db.session.commit()
        current_app.logger.info(f"Successfully created {model_name} with id: {getattr(new_obj, 'id', 'unknown')}")
        return mutation_cls(obj=new_obj)

    Arguments = type("Arguments", (), {"input_data": InputType(required=True)})

    mutation_cls = type(
        f"Create{model_name}Mutation",
        (graphene.Mutation,),
        {
            "Arguments": Arguments,
            "obj": graphene.Field(gql_type),
            "mutate": mutate,
        }
    )
    return mutation_cls


def make_update_mutation(model_name, model_class, gql_type, InputType):
    mutation_cls = None

    def mutate(self, info, id, input_data):
        current_app.logger.debug(f"Attempting update for {model_name} with id {id} and data: {input_data}")
        service = get_service_for_model(model_name)
        if service is not None:
            if not hasattr(service, "update"):
                current_app.logger.error(f"Service for model {model_name} does not implement 'update'")
            current_app.logger.debug(f"Using service for updating {model_name}")
            updated_obj = service.update(id, input_data, info.context)
        else:
            updated_obj = model_class.query.get(id)
            if not updated_obj:
                current_app.logger.error(f"Update failed: {model_name} with id {id} not found")
                raise Exception(f"{model_name} not found")
            for key, value in input_data.items():
                setattr(updated_obj, key, value)
            db.session.commit()
        current_app.logger.info(f"Successfully updated {model_name} with id {id}")
        return mutation_cls(obj=updated_obj)

    Arguments = type("Arguments", (), {"id": graphene.Int(required=True), "input_data": InputType(required=True)})

    mutation_cls = type(
        f"Update{model_name}Mutation",
        (graphene.Mutation,),
        {
            "Arguments": Arguments,
            "obj": graphene.Field(gql_type),
            "mutate": mutate,
        }
    )
    return mutation_cls


def make_delete_mutation(model_name, model_class):
    mutation_cls = None

    def mutate(self, info, id):
        current_app.logger.debug(f"Attempting deletion for {model_name} with id {id}")
        service = get_service_for_model(model_name)
        if service and hasattr(service, "delete"):
            success = service.delete(id, info.context)
        else:
            instance = model_class.query.get(id)
            if not instance:
                current_app.logger.error(f"Deletion failed: {model_name} with id {id} not found")
                raise Exception(f"{model_name} not found")
            db.session.delete(instance)
            db.session.commit()
            success = True
        current_app.logger.info(f"Successfully deleted {model_name} with id {id}")
        return mutation_cls(success=success)

    Arguments = type("Arguments", (), {"id": graphene.Int(required=True)})

    mutation_cls = type(
        f"Delete{model_name}Mutation",
        (graphene.Mutation,),
        {
            "Arguments": Arguments,
            "success": graphene.Boolean(),
            "mutate": mutate,
        }
    )
    return mutation_cls


def generate_mutations():
    mutation_fields = {}
    models = get_all_models()

    for model_name, model_class in models.items():
        gql_type = generate_graphql_type(model_class)

        # Build an InputType for the model based on its columns
        input_fields = {}
        for column in model_class.__table__.columns:
            if column.name == "id":
                continue
            col_type = str(column.type)
            field_type = graphene.String if "VARCHAR" in col_type else graphene.Int
            input_fields[column.name] = field_type()
        # Include an id field for update operations
        input_fields["id"] = graphene.Int()
        InputType = type(f"{model_name}Input", (graphene.InputObjectType,), input_fields)

        create_mutation = make_create_mutation(model_name, model_class, gql_type, InputType)
        update_mutation = make_update_mutation(model_name, model_class, gql_type, InputType)
        delete_mutation = make_delete_mutation(model_name, model_class)

        mutation_fields[f"create{model_name}"] = create_mutation.Field()
        mutation_fields[f"update{model_name}"] = update_mutation.Field()
        mutation_fields[f"delete{model_name}"] = delete_mutation.Field()

    return type("Mutation", (graphene.ObjectType,), mutation_fields)

# app/graphql/schema.py
import graphene
from app.graphql.auto_queries import generate_queries
from app.graphql.auto_mutations import generate_mutations

Query = generate_queries()
Mutation = generate_mutations()

schema = graphene.Schema(query=Query, mutation=Mutation)

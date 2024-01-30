import strawberry
from strawberry.fastapi import GraphQLRouter

from query.query import Query

graphql_schema = strawberry.Schema(query=Query)
graphql_router: GraphQLRouter = GraphQLRouter(graphql_schema)

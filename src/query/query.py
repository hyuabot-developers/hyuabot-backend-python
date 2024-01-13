import strawberry


@strawberry.type
class Query:
    health: bool = strawberry.field(
        resolver=lambda: True,
        description="Health check",
    )


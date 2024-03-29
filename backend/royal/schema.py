import graphene
import graphql_jwt
import users.schema
import questions.schema
import mock_test.schema

class Query(
    users.schema.Query,
    questions.schema.Query,
    mock_test.schema.Query,
    graphene.ObjectType,
):
    pass

class Mutation(
    users.schema.Mutation,
    questions.schema.Mutation,
    mock_test.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
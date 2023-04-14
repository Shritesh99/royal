from django.contrib.auth import get_user_model

import graphene
import graphql_social_auth
from graphql_jwt.shortcuts import get_token
from graphql_jwt.shortcuts import create_refresh_token
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import AppUser
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class AppUserType(DjangoObjectType):
    class Meta:
        model = AppUser
        exclude = ('_id',)

class SocialAuthMutation(graphql_social_auth.SocialAuthMutation):
    user = graphene.Field(AppUserType)
    refresh_token = graphene.String()
    token = graphene.String()

    @classmethod
    def resolve(cls, root, info, social, **kwargs):
        extra_data = social.extra_data
        try:
            user = AppUser.objects.get(user=social.user)
        except err:
            user= None
            print(err)
        if not user:	       
            user = AppUser(user=social.user, picture=extra_data['picture'])
            user.save()
        if social.user.refresh_tokens.count() >= 1:
            refresh_token = social.user.refresh_tokens.last()
        else:
            refresh_token = create_refresh_token(social.user)
        return cls(
            user=user,
            token=get_token(social.user),
            refresh_token=refresh_token
        )

class DobGenderMutation(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        dob = graphene.Date()
        gender = graphene.String()

    @login_required
    def mutate(self, info, dob, gender):
        user = AppUser.objects.get(user=info.context.user)
        if (dob is not None) and (dob != ""):
            user.dob = dob
        if(gender is not None) and (gender != ""):
            user.gender = gender
        user.save()
        return DobGenderMutation(success=True)

class Mutation(graphene.ObjectType):
    social_user = SocialAuthMutation.Field()
    add_dob_gender = DobGenderMutation.Field()

class Query(graphene.ObjectType):
    me = graphene.Field(AppUserType)

    @login_required
    def resolve_me(self, info):
        return AppUser.objects.get(user=info.context.user)
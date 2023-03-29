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

class SocialAuth(graphql_social_auth.SocialAuthMutation):
    user = graphene.Field(AppUserType)
    refresh_token = graphene.String()
    token = graphene.String()

    @classmethod
    def resolve(cls, root, info, social, **kwargs):
        extra_data = social.extra_data
        user = AppUser.objects.filter(user=social.user)
        if not user:	       
            user = AppUser(user=social.user, picture=extra_data['picture'])
            user.save()
        else: 
            user = user.first()
        if social.user.refresh_tokens.count() >= 1:
            refresh_token = social.user.refresh_tokens.last()
        else:
            refresh_token = create_refresh_token(social.user)
        return cls(
            user=user,
            token=get_token(social.user),
            refresh_token=refresh_token
        )

class DobGender(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        dob = graphene.Date()
        gender = graphene.String()

    @login_required
    def mutate(self, info, dob, gender):
        user = AppUser.objects.filter(user=info.context.user).first()
        user.dob = dob
        user.gender = gender
        user.save()
        return DobGender(success=True)

class Mutation(graphene.ObjectType):
    social_user = SocialAuth.Field()
    add_dob_gender = DobGender.Field()

class Query(graphene.ObjectType):
    me = graphene.Field(AppUserType)

    @login_required
    def resolve_me(self, info):
        user = AppUser.objects.filter(user=info.context.user).first()
        return user
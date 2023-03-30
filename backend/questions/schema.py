import graphene
from graphene_django import DjangoObjectType
from questions.models import *
from graphql_jwt.decorators import login_required

class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice 

class FSLSMQuestionType(DjangoObjectType):
    class Meta:
        model = FSLSMQuestion

class Query(graphene.ObjectType):
    fslsm_questions = graphene.List(FSLSMQuestionType)

    @login_required
    def resolve_fslsm_questions(self, info):
        return FSLSMQuestion.objects.all()
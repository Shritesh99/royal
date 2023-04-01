import graphene
from graphene_django import DjangoObjectType
from questions.models import *
from graphql_jwt.decorators import login_required
from users.models import AppUser

class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice 

class FSLSMQuestionType(DjangoObjectType):
    class Meta:
        model = FSLSMQuestion

class FSLSMQuestionInput(graphene.InputObjectType):
    question = graphene.Int()
    answer = graphene.String()

class FSLSMQuestionsMutation(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        response = graphene.List(FSLSMQuestionInput)
    
    @login_required
    def mutate(self, info, response):
        user = AppUser.objects.filter(user = info.context.user).first()
        res = {}
        for item in response:
            res[item.question] = Choice.objects.filter(id=item.answer).first().text
        user.ls = ""
        user.save()
        return FSLSMQuestionsMutation(success=True)

class Mutation(graphene.ObjectType):
    add_FSLSMQuestions_response = FSLSMQuestionsMutation.Field()

class Query(graphene.ObjectType):
    fslsm_questions = graphene.List(FSLSMQuestionType)

    @login_required
    def resolve_fslsm_questions(self, info):
        return FSLSMQuestion.objects.all()
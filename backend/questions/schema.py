import graphene
from graphene_django import DjangoObjectType
from questions.models import *
from graphql_jwt.decorators import login_required
from users.models import AppUser
from ml.MLE_LearningModel import determine_learning_style

class ChoiceType(DjangoObjectType):
    class Meta:
        model = FSLSMChoice

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
        user = AppUser.objects.get(user = info.context.user)
        res = {}
        for item in response:
            res[str(item.question)] = "A" if FSLSMQuestion.objects.get(order=item.question).choices.first().id == item.answer else "B"
        user.ls = determine_learning_style(res)
        user.save()
        return FSLSMQuestionsMutation(success=True)

class Mutation(graphene.ObjectType):
    add_FSLSMQuestions_response = FSLSMQuestionsMutation.Field()

class Query(graphene.ObjectType):
    fslsm_questions = graphene.List(FSLSMQuestionType)

    @login_required
    def resolve_fslsm_questions(self, info):
        return FSLSMQuestion.objects.all()
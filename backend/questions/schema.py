import graphene
from graphene_django import DjangoObjectType
from questions.models import *
from graphql_jwt.decorators import login_required
from users.models import AppUser
from ml.MLE_LearningModel import determine_learning_style
from ml.motivitation import calculate_score


class ChoiceType(DjangoObjectType):
    class Meta:
        model = FSLSMChoice


class FSLSMQuestionType(DjangoObjectType):
    class Meta:
        model = FSLSMQuestion


class FSLSMQuestionInput(graphene.InputObjectType):
    question = graphene.String()
    answer = graphene.String()


class MotivationQuestionType(DjangoObjectType):
    class Meta:
        model = MotivationQuestion


class MotivationQuestionInput(graphene.InputObjectType):
    question = graphene.String()
    answer = graphene.Int()


class FSLSMQuestionsMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        response = graphene.List(FSLSMQuestionInput)

    @login_required
    def mutate(self, info, response):
        user = AppUser.objects.get(user=info.context.user)
        res = {}
        for item in response:
            res[item.question] = "A" if FSLSMQuestion.objects.get(
                order=item.question).choices.first().id == item.answer else "B"
        user.ls = determine_learning_style(user.user.id, res)
        user.save()
        return FSLSMQuestionsMutation(success=True)


class MotivationQuestionsMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        response = graphene.List(MotivationQuestionInput)

    @login_required
    def mutate(self, info, response):
        user = AppUser.objects.get(user=info.context.user)
        res = {}
        for item in response:
            res['Q'+item.question] = item.answer
        user.mv_score = calculate_score(user.user.id, res)
        user.save()
        return MotivationQuestionsMutation(success=True)


class Mutation(graphene.ObjectType):
    add_FSLSMQuestions_response = FSLSMQuestionsMutation.Field()
    add_MotivationQuestions_response = MotivationQuestionsMutation().Field()


class Query(graphene.ObjectType):
    fslsm_questions = graphene.List(FSLSMQuestionType)
    motivation_questions = graphene.List(MotivationQuestionType)

    @login_required
    def resolve_fslsm_questions(self, info):
        return FSLSMQuestion.objects.all()

    @login_required
    def resolve_motivation_questions(self, info):
        return MotivationQuestion.objects.all()

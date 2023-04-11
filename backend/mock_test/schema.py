import random
import graphene
from graphene_django import DjangoObjectType
from mock_test.models import *
from graphql_jwt.decorators import login_required
from users.models import AppUser
from questions.models import GREQuestion
from mock_test.models import MockTest
from django.db.models import Count

class GREChoices(DjangoObjectType):
    class Meta:
        model = Choice
        exclude = ('is_correct',)
class GREQuestionInTestType(DjangoObjectType):
    class Meta:
        model = GREQuestion
        exclude = ('difficulty', 'subjects',)

class QuestionsType(graphene.ObjectType):
    success = graphene.Boolean()
    test_id = graphene.String()
    questions = graphene.List(GREQuestionInTestType)

class TestInteractionInput(graphene.InputObjectType):
    questionId = graphene.String()
    choiceId = graphene.String()
    time_taken = graphene.Int()

class SubmmitTestMutation(graphene.Mutation):
    success = graphene.Boolean()
    
    class Arguments:
        testId = graphene.String()
        response = graphene.List(TestInteractionInput)
    @login_required
    def mutate(self, info, testId, response):
        mock_test = MockTest.objects.get(id=testId)
        for item in response:
            question=GREQuestion.objects.get(id=item.questionId)
            correct = question.choices.get(id=item.choiceId).is_correct
            interaction = QuestionInteraction.objects.create(question=question, correct=correct, time_taken=item.time_taken)
            mock_test.interactions.add(interaction)
            mock_test.save()
        return SubmmitTestMutation(success = True)

class ExamMutation(graphene.Mutation):
    success = graphene.Boolean()
    test_id = graphene.String()
    question = graphene.Field(GREQuestionInTestType)

    class Arguments:
        first = graphene.Boolean()
        testId = graphene.String()
        questionId = graphene.String()
        choiceId = graphene.String()
        time_taken = graphene.Int()

    @login_required
    def mutate(self, info, first, testId, questionId, choiceId, time_taken):
        if first:
            num_questions_per_difficulty = 2
            difficulty_levels = GREQuestion.objects.values_list('difficulty', flat=True).distinct()
            questions = []

            for level in difficulty_levels:
                qs = GREQuestion.objects.filter(difficulty=level).annotate(num_choices=Count('choices'))
                question_ids = [q.id for q in qs if q.num_choices > 0]
                if len(question_ids) >= num_questions_per_difficulty:
                    questions.extend(random.sample(question_ids, num_questions_per_difficulty))
                else:
                    questions.extend(question_ids)

            selected_questions = list(GREQuestion.objects.filter(id__in=questions))
            random.shuffle(selected_questions)
            mock_test = MockTest.objects.create()
            mock_test.questions.add(*selected_questions)
            mock_test.save()
            user = AppUser.objects.get(user = info.context.user)
            user.mock_tests.add(mock_test)
            user.save()
            return ExamMutation(question=mock_test.questions.first(), test_id = mock_test.id)
        mock_test = MockTest.objects.get(id=testId)
            
        question=GREQuestion.objects.get(id=questionId)
        correct = question.choices.get(id=choiceId).is_correct
        interaction = QuestionInteraction.objects.create(question=question, correct=correct, time_taken=time_taken)
        mock_test.interactions.add(interaction)
        mock_test.save()
        
        for intractionObj in mock_test.interactions.all():
            for ques in mock_test.questions.all():
                if ques.id is not intractionObj.question.id:
                    return ExamMutation(question=ques,test_id = mock_test.id)
        return ExamMutation(question=None, test_id = mock_test.id)

class Query(graphene.ObjectType):
    test = graphene.Field(QuestionsType, testId=graphene.String(required=False))

    @login_required
    def resolve_test(self, info, testId):
        if testId is not None and testId != "":
            mock_test = MockTest.objects.get(id=testId)
            return QuestionsType(success=True, test_id=mock_test.id, questions= mock_test.questions.all())
        num_questions_per_difficulty = 2
        difficulty_levels = GREQuestion.objects.values_list('difficulty', flat=True).distinct()
        questions = []

        for level in difficulty_levels:
            qs = GREQuestion.objects.filter(difficulty=level).annotate(num_choices=Count('choices'))
            question_ids = [q.id for q in qs if q.num_choices > 0]
            if len(question_ids) >= num_questions_per_difficulty:
                questions.extend(random.sample(question_ids, num_questions_per_difficulty))
            else:
                questions.extend(question_ids)

        selected_questions = list(GREQuestion.objects.filter(id__in=questions))
        random.shuffle(selected_questions)
        mock_test = MockTest.objects.create()
        mock_test.questions.add(*selected_questions)
        mock_test.save()
        user = AppUser.objects.get(user = info.context.user)
        user.mock_tests.add(mock_test)
        user.save()
        return QuestionsType(success=True, test_id=mock_test.id, questions=mock_test.questions.all())


class Mutation(graphene.ObjectType):
    take_test = ExamMutation.Field()
    submit_test = SubmmitTestMutation.Field()
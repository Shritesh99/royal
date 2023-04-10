import random
import graphene
from graphene_django import DjangoObjectType
from mock_test.models import *
from graphql_jwt.decorators import login_required
from users.models import AppUser
from questions.models import GREQuestion
from mock_test.models import MockTest
import channels_graphql_ws
from django.db.models import Count

class GREQuestionInTestType(DjangoObjectType):
    class Meta:
        model = GREQuestion
        exclude = ('difficulty', 'subjects',)

class QuestionInteractionType(DjangoObjectType):
    class Meta:
        model = QuestionInteraction
        
class MockTestType(DjangoObjectType):
    class Meta:
        model = MockTest

class QuestionInteractionInputType(graphene.InputObjectType):
    first = graphene.Boolean()
    questionId = graphene.String()
    choiceId = graphene.String()

class MockTestSubscription(channels_graphql_ws.Subscription):
    notification_queue_limit = 64
    
    question = graphene.Field(GREQuestionInTestType)
    
    class Arguments:
        first = graphene.Boolean()
        testId = graphene.String()
        questionId = graphene.String()
        choiceId = graphene.String()
        time_taken = graphene.Int()
        
    @staticmethod
    def subscribe(root, info, arg1, arg2):
        """Called when user subscribes."""

        # Return the list of subscription group names.
        return ["group42"]
    # @login_required
    @staticmethod
    def publish(payload, info, first, testId, questionId, choiceId, time_taken):
        mock_test = MockTest.objects.get(id=testId)
        if first:
            return MockTestSubscription(question=mock_test.questions.first())
        question=GREQuestion.objects.get(id=questionId)
        correct = question.choices.get(id=choiceId).is_correct
        interaction = QuestionInteraction.objects.create(question=question, correct=correct, time_taken=time_taken)
        mock_test.interactions.add(interaction)
        mock_test.save()
        
        for intractionObj in mock_test.interactions:
            for ques in mock_test.questions:
                if ques.id is not intractionObj.question.id:
                    return MockTestSubscription(question=ques)
        return MockTestSubscription(question=None)

class StartTestMutation(graphene.Mutation):
    success = graphene.Boolean()
    test_id = graphene.String()
    
    # @login_required
    def mutate(self, info):
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
        # user = AppUser.objects.get(user = info.context.user)
        # user.mock_tests.add(mock_test)
        # user.save()
        return StartTestMutation(success = True, test_id = mock_test.id)

class Mutation(graphene.ObjectType):
    start_test = StartTestMutation.Field()

class Subscription(graphene.ObjectType):
    mock_test = MockTestSubscription.Field()
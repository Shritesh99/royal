import random
import graphene
from graphene_django import DjangoObjectType
from mock_test.models import *
from graphql_jwt.decorators import login_required
from users.models import AppUser
from questions.models import GREQuestion
from mock_test.models import MockTest
from django.db.models import Count
from ml.gpt import get_question
from ml.extract_skill_level import extra_skill_level

difficulty_labels = {"Easy": 1, "Medium": 3, "Hard": 5}


class GREChoices(DjangoObjectType):
    class Meta:
        model = Choice
        exclude = ('is_correct',)


class GREQuestionInTestType(DjangoObjectType):
    class Meta:
        model = GREQuestion
        exclude = ('difficulty', 'topic',)


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
        gre_answers = []
        total_time = 0
        for item in response:
            question = GREQuestion.objects.get(id=item.questionId)
            correct = question.choices.get(id=item.choiceId).is_correct
            interaction = QuestionInteraction.objects.create(
                question=question, correct=correct, time_taken=item.time_taken)
            mock_test.interactions.add(interaction)
            total_time += item.time_taken
            gre_answers.append({
                'Topic': question.topic.no,
                'time': item.time_taken,
                'difficulty': question.difficulty,
                'correct': 1 if correct else 0
            })
        mock_test.time_taken = total_time
        mock_test.save()
        user = AppUser.objects.get(user=info.context.user)
        user.is_first_test = False
        user.save()
        extra_skill_level(user.user.id, gre_answers)
        return SubmmitTestMutation(success=True)


class ExamMutation(graphene.Mutation):
    success = graphene.Boolean()
    test_id = graphene.String()
    question = graphene.Field(GREQuestionInTestType)

    class Arguments:
        testId = graphene.String()
        questionId = graphene.String()
        choiceId = graphene.String()
        time_taken = graphene.Int()

    @login_required
    def mutate(self, info, testId, questionId, choiceId, time_taken):
        user = AppUser.objects.get(user=info.context.user)
        if user.is_first_test:
            num_questions_per_difficulty = 2
            difficulty_levels = GREQuestion.objects.values_list(
                'difficulty', flat=True).distinct()
            questions = []

            for level in difficulty_levels:
                qs = GREQuestion.objects.filter(difficulty=level).annotate(
                    num_choices=Count('choices'))
                question_ids = [q.id for q in qs if q.num_choices > 0]
                if len(question_ids) >= num_questions_per_difficulty:
                    questions.extend(random.sample(
                        question_ids, num_questions_per_difficulty))
                else:
                    questions.extend(question_ids)

            selected_questions = list(
                GREQuestion.objects.filter(id__in=questions))
            random.shuffle(selected_questions)
            mock_test = MockTest.objects.create()
            mock_test.questions.add(*selected_questions)
            mock_test.save()
            user.mock_tests.add(mock_test)
            user.save()
            return ExamMutation(question=mock_test.questions.first(), test_id=mock_test.id)
        mock_test = MockTest.objects.get(id=testId)

        question = GREQuestion.objects.get(id=questionId)
        correct = question.choices.get(id=choiceId).is_correct
        interaction = QuestionInteraction.objects.create(
            question=question, correct=correct, time_taken=time_taken)
        mock_test.interactions.add(interaction)
        mock_test.save()

        for intractionObj in mock_test.interactions.all():
            for ques in mock_test.questions.all():
                if ques.id is not intractionObj.question.id:
                    return ExamMutation(question=ques, test_id=mock_test.id)
        return ExamMutation(question=None, test_id=mock_test.id)


class Query(graphene.ObjectType):
    test = graphene.Field(
        QuestionsType, testId=graphene.String(required=False))

    @login_required
    def resolve_test(self, info, testId):
        user = AppUser.objects.get(user=info.context.user)
        if testId is not None and testId != "":
            mock_test = MockTest.objects.get(id=testId)
            return QuestionsType(success=True, test_id=mock_test.id, questions=mock_test.questions.all())
        if user.is_first_test:
            num_questions_per_difficulty = 2
            difficulty_levels = GREQuestion.objects.values_list(
                'difficulty', flat=True).distinct()
            questions = []

            for level in difficulty_levels:
                qs = GREQuestion.objects.filter(difficulty=level).annotate(
                    num_choices=Count('choices'))
                question_ids = [q.id for q in qs if q.num_choices > 0]
                if len(question_ids) >= num_questions_per_difficulty:
                    questions.extend(random.sample(
                        question_ids, num_questions_per_difficulty))
                else:
                    questions.extend(question_ids)

            selected_questions = list(
                GREQuestion.objects.filter(id__in=questions))
            random.shuffle(selected_questions)
            mock_test = MockTest.objects.create()
            mock_test.questions.add(*selected_questions)
            mock_test.save()
            user.mock_tests.add(mock_test)
            user.save()
            return QuestionsType(success=True, test_id=mock_test.id, questions=mock_test.questions.all())
        # TODO: ChatGPT based tests
        num_questions_per_difficulty = 2
        difficulty_levels = GREQuestion.objects.values_list(
            'difficulty', flat=True).distinct()
        questions = []

        for i in range(10):
            get_difficulty, question, options, answer_index, explanation, ontology_tags = get_question(
                user.user.id)
            grequestion = GREQuestion()
            grequestion.text = question
            grequestion.difficulty = difficulty_labels[get_difficulty]
            grequestion.topic = ontology_tags[0]
            for i in range(len(options)):
                choice = Choice()
                choice.text = options[i]
                choice.is_correct = i == answer_index
                choice.save()
                grequestion.choices.add(choice)
            grequestion.save()
            questions.append(grequestion)
        random.shuffle(questions)
        mock_test = MockTest.objects.create()
        mock_test.questions.add(*question)
        mock_test.save()
        user = AppUser.objects.get(user=info.context.user)
        user.mock_tests.add(mock_test)
        user.save()
        return QuestionsType(success=True, test_id=mock_test.id, questions=mock_test.questions.all())


class Mutation(graphene.ObjectType):
    take_test = ExamMutation.Field()
    submit_test = SubmmitTestMutation.Field()

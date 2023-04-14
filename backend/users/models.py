from django.utils import timezone
from djongo import models
from django.contrib.auth import get_user_model

from mock_test.models import *
# Create your models here.


class UserInteraction(models.Model):
    timestamp = models.DateTimeField()
    login_timestamp = models.DateTimeField()
    time_spent_today = models.IntegerField()
    total_questions_today = models.IntegerField()
    accuracy_today = models.FloatField()


class UserPerformance(models.Model):
    avg_accuracy = models.FloatField()
    avg_time = models.IntegerField()
    avg_question_daily = models.IntegerField()
    total_score = models.IntegerField()


class AppUser(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)
    picture = models.URLField(null=True)
    ls = models.CharField(null=True, max_length=100)
    is_first_test = models.BooleanField(default=True)
    user_interaction = models.ForeignKey(
        UserInteraction, on_delete=models.SET_NULL, null=True)
    user_performance = models.ForeignKey(
        UserPerformance, on_delete=models.SET_NULL, null=True)
    mock_tests = models.ManyToManyField(MockTest, blank=True)
    motivation = models.CharField(max_length=10, null=True)

    class Meta:
        verbose_name = 'Social Auth'
        verbose_name_plural = 'Social Auths'

    def __str__(self):
        return str(self.user.username)

from djongo import models
from questions.models import *
# Create your models here.

class QuestionInteraction(models.Model):
    question = models.ForeignKey(GREQuestion, on_delete=models.SET_NULL, null=True)
    correct = models.BooleanField()
    time_taken = models.IntegerField(default=0)

class MockTest(models.Model):
    questions = models.ManyToManyField(GREQuestion, blank=True)
    duration = models.IntegerField(default=30, help_text="Duration in Minutes")
    time_taken = models.IntegerField(default=0, blank=True)
    interactions = models.ManyToManyField(QuestionInteraction, blank=True)
    score = models.IntegerField(default=0, blank=True)
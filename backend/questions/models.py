from djongo import models

# Create your models here.

class Choice(models.Model):
    text = models.TextField(blank=False)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
        
    def __str__(self):
        return str(self.text)

class FSLSMChoice(models.Model):
    text = models.TextField(blank=False)

    class Meta:
        verbose_name = 'FSLSM Choice'
        verbose_name_plural = 'FSLSM Choices'
        
    def __str__(self):
        return str(self.text)
    
class GREQuestion(models.Model):
    text = models.TextField(blank=False)
    difficulty = models.IntegerField(blank=False, default=1, help_text="Difficulty on the scale of 1-5, 5 being the most difficult") # 1-5 (5 hard)
    choices = models.ManyToManyField(Choice, blank=True)
    
    class Meta:
        verbose_name = 'GRE Question'
        verbose_name_plural = 'GRE Questions'
    
    def __str__(self):
        return str(self.text)
    
    @property
    def get_tags(self):
        return self.tags.all()

class FSLSMQuestion(models.Model):
    order = models.IntegerField(unique=True, null=False)
    text = models.TextField(blank=False)
    choices = models.ManyToManyField(FSLSMChoice, blank=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'FSLSM Question'
        verbose_name_plural = 'FLSM Questions'
    
    def __str__(self):
        return str(self.text)

# class Goal(models.Model):
#     topic_name = models.CharField(max_length=255)
#     goal_accuracy = models.FloatField()
#     total_questions = models.IntegerField()


# class SubjectGoal(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    
# class GlobalGoal(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     total_score = models.IntegerField()
#     total_accuracy = models.FloatField()
    

# class SubjectGoalAchievement(models.Model):
#     user_interaction = models.ForeignKey(UserInteraction, on_delete=models.CASCADE)
#     goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    
# class GlobalGoalAchievement(models.Model):
#     user_interaction = models.ForeignKey(UserInteraction, on_delete=models.CASCADE)
#     global_goal = models.ForeignKey(GlobalGoal, on_delete=models.CASCADE)

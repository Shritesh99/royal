from djongo import models

# Create your models here.
from taggit.managers import TaggableManager

class Choice(models.Model):
    _id = models.ObjectIdField()
    text = models.TextField(blank=False)
    
    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
    
    def __str__(self):
        return str(self._id)


class GREQuestion(models.Model):
    _id = models.ObjectIdField()
    text = models.TextField(blank=False)
    answer = models.OneToOneField(Choice, on_delete=models.CASCADE, related_name="Answer")
    difficulty = models.IntegerField(blank=False, default=1) # 1-5 (5 hard)
    choices = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="Choices")
    tags = TaggableManager()
    
    class Meta:
        verbose_name = 'GRE Question'
        verbose_name_plural = 'GRE Questions'
    
    def __str__(self):
        return str(self._id)
    
    @property
    def get_tags(self):
        return self.tags.all()

class FSLSMQuestion(models.Model):
    _id = models.Model
    order = models.IntegerField(unique=True, null=False)
    text = models.TextField(blank=False)
    choices = models.ForeignKey(Choice, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'FSLSM Question'
        verbose_name_plural = 'FLSM Questions'
    
    def __str__(self):
        return str(self._id)
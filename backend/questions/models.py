from djongo import models

# Create your models here.
from taggit.managers import TaggableManager

class Choice(models.Model):
    text = models.TextField(blank=False)
    
    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
        
    def __str__(self):
        return str(self.text)


class GREQuestion(models.Model):
    text = models.TextField(blank=False)
    answer = models.OneToOneField(Choice, null=True, on_delete=models.SET_NULL, related_name="Answer")
    difficulty = models.IntegerField(blank=False, default=1) # 1-5 (5 hard)
    choices = models.ManyToManyField(Choice, blank=True)
    tags = TaggableManager()
    
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
    choices = models.ManyToManyField(Choice, blank=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'FSLSM Question'
        verbose_name_plural = 'FLSM Questions'
    
    def __str__(self):
        return str(self.text)
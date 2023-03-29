from django.utils import timezone
from djongo import models
from django.contrib.auth import get_user_model

# Create your models here.

class AppUser(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)
    picture = models.URLField(null=True)
    ls = models.CharField(null=True, max_length=100)

    class Meta:
        verbose_name = 'Social Auth'
        verbose_name_plural = 'Social Auths'
    
    def __str__(self):
        return str(self._id)

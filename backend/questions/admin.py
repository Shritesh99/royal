from django.contrib import admin
from questions.models import *

# Register your models here.
admin.site.register(FSLSMChoice)
admin.site.register(Choice)
admin.site.register(Topic)
admin.site.register(GREQuestion)
admin.site.register(FSLSMQuestion)
admin.site.register(MotivationQuestion)
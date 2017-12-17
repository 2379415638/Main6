from django.contrib import admin
from notes import models
# Register your models here.
admin.site.register(models.Topic)
admin.site.register(models.Content)
admin.site.register(models.User)
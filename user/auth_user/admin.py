from django.contrib import admin
from django.contrib.auth import get_user_model

NewUser = get_user_model()
# Register your models here.
admin.site.register(NewUser)

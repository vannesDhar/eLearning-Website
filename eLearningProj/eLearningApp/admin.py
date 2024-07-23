# accounts/admin.py
from django.contrib import admin

from .models import *
from django.contrib.auth.models import Permission

admin.site.register(User)
admin.site.register(Course) 
admin.site.register(Enrollment)
admin.site.register(CourseMaterial)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(Feedback)
# admin.site.register(Permission)


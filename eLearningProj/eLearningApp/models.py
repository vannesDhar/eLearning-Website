from django.db import models
import os
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    isStudent = models.BooleanField(default=False)
    isTeacher = models.BooleanField(default=False)


class Course(models.Model):
    DIFFICULTY_LEVEL = (
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    )
     
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=DIFFICULTY_LEVEL)

    def __str__(self):
        return self.name
    
class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    file =  models.FileField(blank=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    picture = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Delete the old picture if this profile already has one
        try:
            old_profile = Profile.objects.get(pk=self.pk)
            if old_profile.picture:
                if self.picture != old_profile.picture:
                    if os.path.isfile(old_profile.picture.path):
                        os.remove(old_profile.picture.path)
        except Profile.DoesNotExist:
            pass

        # Call the original save method
        super().save(*args, **kwargs)
            
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Feedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) 
    comments = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"

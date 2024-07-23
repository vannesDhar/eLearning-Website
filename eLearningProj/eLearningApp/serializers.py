from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    teacher_username = serializers.ReadOnlyField(source='teacher.username')
    class Meta:
        model = Course
        fields = ['id','name', 'teacher', 'teacher_username', 'description', 'level']

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ['id','course','title', 'description', 'file']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'isStudent', 'isTeacher']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
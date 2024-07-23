from rest_framework import generics
from .models import User, Course, CourseMaterial, Profile, Enrollment, Feedback, Notification
from .serializers import UserSerializer, CourseSerializer, CourseMaterialSerializer, ProfileSerializer, EnrollmentSerializer, FeedbackSerializer, NotificationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import status

@api_view(['GET'])
def api_root(request, format=None):
    """
    List all available API endpoints.
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'user-detail': reverse('user-detail', kwargs={'pk': 1}, request=request, format=format),  # Example with pk=1
        'courses': reverse('course-list', request=request, format=format),
        'course-detail': reverse('course-detail', kwargs={'pk': 1}, request=request, format=format),  # Example with pk=1
        'course-materials': reverse('course-material-list', request=request, format=format),
        'course-material-detail': reverse('course-material-detail', kwargs={'pk': 1}, request=request, format=format),  # Example with pk=1
        'profiles': reverse('profile-list', request=request, format=format),
        'profile-detail': reverse('profile-detail', kwargs={'pk': 1}, request=request, format=format),  # Example with pk=1
        'enrollments': reverse('enrollment-list', request=request, format=format),
        'enrollment-detail': reverse('enrollment-detail', kwargs={'pk': 1}, request=request, format=format),  # Example with pk=1
        'feedbacks': reverse('feedback-list', request=request, format=format),
        'feedback-detail': reverse('feedback-detail', kwargs={'pk': 1}, request=request, format=format),  # Example with pk=1
        'notifications': reverse('notification-list', request=request, format=format),
        'notification-detail': reverse('notification-detail', kwargs={'pk': 1}, request=request, format=format),  # Example with pk=1
    })

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseMaterialListView(generics.ListCreateAPIView):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer

class CourseMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer

class ProfileListView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class EnrollmentListView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class FeedbackListView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.api_root, name='api-root'),
    path('users/', api_views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', api_views.UserDetailView.as_view(), name='user-detail'),
    path('courses/', api_views.CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', api_views.CourseDetailView.as_view(), name='course-detail'),
    path('course-materials/', api_views.CourseMaterialListView.as_view(), name='course-material-list'),
    path('course-materials/<int:pk>/', api_views.CourseMaterialDetailView.as_view(), name='course-material-detail'),
    path('profiles/', api_views.ProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', api_views.ProfileDetailView.as_view(), name='profile-detail'),
    path('enrollments/', api_views.EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/<int:pk>/', api_views.EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('feedbacks/', api_views.FeedbackListView.as_view(), name='feedback-list'),
    path('feedbacks/<int:pk>/', api_views.FeedbackDetailView.as_view(), name='feedback-detail'),
    path('notifications/', api_views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', api_views.NotificationDetailView.as_view(), name='notification-detail'),
]
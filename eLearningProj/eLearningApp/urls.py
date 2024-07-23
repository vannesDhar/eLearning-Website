from django.contrib import admin
from django.urls import path, include
from . import views
from . import consumers
urlpatterns = [
    path('home/', views.homepage, name='homepage'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create_course/', views.create_course, name='create_course'),
    path('enroll/<int:course_id>', views.enroll, name='enroll'),
    path('view_course/<int:course_id>', views.view_course, name='view_course'),
    path('create_material/<int:course_id>', views.create_material, name='create_material'),
    path('delete_course/<int:course_id>', views.delete_course, name='delete_course'),
    path('delete_material/<int:mat_id>', views.delete_material, name='delete_material'),
    path('search/', views.search, name='search'),
    path('view_user/<int:user_id>', views.view_user, name='view_user'),
    path('remove_student/<int:course_id>/<int:student_id>', views.remove_student, name='remove_student'),
    path('leave_feedback/<int:course_id>', views.leave_feedback, name='leave_feedback'),
    path('home/inbox/', views.inbox, name='inbox'),
]

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer),
]
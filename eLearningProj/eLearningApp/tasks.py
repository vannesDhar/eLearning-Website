from celery import shared_task
from django.core.mail import send_mail
from .models import User, Enrollment, CourseMaterial, Notification

@shared_task
def send_material_notification(course_id):
    enrolled_users = Enrollment.objects.filter(course_id=course_id).values_list('student', flat=True)
    latest_material = CourseMaterial.objects.filter(course_id=course_id).latest('id')
    for user_id in enrolled_users:
        user = User.objects.get(pk=user_id)
        notification = Notification(user=user, message=f"New material '{latest_material.title}' uploaded for the course.")
        notification.save()
        



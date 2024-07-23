from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, ProfileForm, CourseForm, MaterialForm, SearchForm, FeedbackForm
from .models import Profile, Course, Enrollment, CourseMaterial, User, Feedback, Notification
from .serializers import CourseSerializer, CourseMaterialSerializer
from django.core.exceptions import ObjectDoesNotExist
from .tasks import send_material_notification


# Homepage 
@api_view(['GET','POST'])
def homepage(request):
    # Checking user authentication
    if request.user.is_authenticated:
        # Splitting into teacher or student
        if request.user.isTeacher:
            # Render the 
            teacher_courses = Course.objects.filter(teacher=request.user)
            teacher_courses_serialized = CourseSerializer(teacher_courses, many=True).data
            return render(request, 'home.html', {'teacher_courses': teacher_courses_serialized})
        else:
            
            enrolled_course_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
            enrolled_courses = Course.objects.filter(pk__in=enrolled_course_ids)
            enrolled_course_serialized = CourseSerializer(enrolled_courses, many=True).data

            available_courses = Course.objects.exclude(id__in=enrolled_courses)
            student_courses_serialized = CourseSerializer(available_courses, many=True).data
            
            return render(request, 'home.html', {'student_courses': student_courses_serialized, 'enrolled_courses': enrolled_course_serialized})
    else:
        return render(request, 'home.html')


def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('../home')
        else:

            return redirect ('registration/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('../home')  # Redirect to home page after successful login
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('../home')


def profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            return redirect('homepage')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user  # Set the current user as the teacher
            course.save()
            return redirect('homepage')  # Redirect to home page or course detail page
    else:
        form = CourseForm()
    return render(request, 'course/create_course.html', {'form': form})

def delete_course(request, course_id):
    if request.method == 'POST':
        # Retrieve the course object from the database
        course = get_object_or_404(Course, pk=course_id)
        # Delete the course
        course.delete()
    # Redirect to a relevant page after course removal
    return redirect('homepage')  

def enroll(request, course_id):
    if request.method == 'POST':
        # Get the current user
        user = request.user
        # Get the course object or return 404 if not found
        course = get_object_or_404(Course, pk=course_id)
        # Create an enrollment instance
        enrollment = Enrollment.objects.create(student=user, course=course)
                # Retrieve the teacher of the course
        teacher = enrollment.course.teacher
        course_name = course.name
        # Create notification for the teacher
        message = f"New student enrolled in your course '{course_name}':{enrollment.student.username}"
        Notification.objects.create(user=teacher, message=message)

        return redirect('homepage')  # Redirect to home page or course detail page
    

def view_course(request,course_id):
    materials = CourseMaterial.objects.filter(course_id=course_id)
    serializer = CourseMaterialSerializer(materials, many=True)
    enrolled = Enrollment.objects.filter(course_id=course_id)
    form = FeedbackForm()
    feedbacks = Feedback.objects.filter(course_id=course_id)
    if materials.exists():
        return render(request, 'course/view_course.html', {'enroll':enrolled,
                                                           'materials': serializer.data, 
                                                           'course_id': course_id,
                                                           'feedbacks': feedbacks,
                                                           'form':form})
    else:
        return render(request, 'course/view_course.html', {'enroll':enrolled,
                                                           'materials': None, 
                                                           'course_id' : course_id,
                                                           'feedbacks': feedbacks, 
                                                           'form':form})

            
def create_material(request, course_id):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, initial={'course': course_id})
        if form.is_valid():
            material = form.save(commit=False)
            material.course_id = course_id
            material.save()
            send_material_notification.delay(course_id)
            return redirect('view_course', course_id=course_id)
        
    return redirect('view_course', course_id=course_id)  # Redirect even if the form is not valid

def delete_material(request, mat_id):
    material = get_object_or_404(CourseMaterial, pk=mat_id)
    material.delete()
    return redirect('view_course', course_id=material.course_id)


def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            # Perform the search query
            results = User.objects.filter(username__icontains=query).exclude(pk=request.user.pk)
            return render(request, 'search_results.html', {'results': results})

def view_user(request, user_id):
    user = User.objects.get(pk=user_id)
    try:
        user = User.objects.get(pk=user_id)
        profile = Profile.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        profile = None
    # Retrieve enrolled courses if the user is a student
    enrolled_courses = None
    if user.isStudent:
        enrolled_courses = Course.objects.filter(enrollment__student=user)
    # Retrieve produced courses if the user is a teacher
    produced_courses = None
    if user.isTeacher:
        produced_courses = Course.objects.filter(teacher=user)
    return render(request, 'user_profile.html', {'user': user, 
                                                 'profile':profile,
                                                 'enrolled_courses': enrolled_courses,
                                                 'produced_courses': produced_courses})

def remove_student(request,course_id,student_id):
    enrollment = get_object_or_404(Enrollment, course_id=course_id, student_id=student_id)
    enrollment.delete()
    return redirect('view_course', course_id=course_id)

def leave_feedback(request, course_id):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user
            feedback.course_id = course_id
            feedback.save()
            return redirect('view_course', course_id=course_id)
    # Return a redirect in case of invalid form data or non-POST request
    return redirect('view_course',course_id=course_id)

def inbox(request):
    if request.user.is_authenticated:
        if request.user.isTeacher:
            notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        elif request.user.isStudent:
            notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'inbox.html', {'notifications': notifications})
    return render(request, 'inbox.html', {'notifications': None})
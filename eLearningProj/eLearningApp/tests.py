from django.test import TestCase, Client
from django.urls import reverse
from eLearningApp.models import *
from eLearningApp.forms import *
from .models import *


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_teacher = User.objects.create_user(username='testteacher', password='12345', isTeacher=True)
        self.user_student = User.objects.create_user(username='teststudent', password='12345', isTeacher=False)
        self.client.login(username='testteacher', password='12345')
        self.course = Course.objects.create(name='Test Course', teacher=self.user_teacher)
        self.profile_teacher = Profile.objects.create(user=self.user_teacher, bio='Test bio for teacher')
        self.profile_student = Profile.objects.create(user=self.user_student, bio='Test bio for student')
        self.enrollment = Enrollment.objects.create(student=self.user_student, course=self.course)
        self.material = CourseMaterial.objects.create(title='Test Material', course=self.course)
        self.notification = Notification.objects.create(user=self.user_student, message='Test notification')
        
    def test_user_signup_post(self):
        # Simulate a POST request to the signup view
        response = self.client.post(reverse('signup'), {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser1',
            'email': 'testuser@gmail.com',
            'password1': 'asdBBS123',
            'password2': 'asdBBS123',
            'user_type': 'teacher',
        })

        # Check if the response redirects to the home page
        self.assertEqual(response.status_code, 302)

        # Check if the user is created in the database
        self.assertTrue(User.objects.filter(username='testuser1').exists())

    def test_user_signup_get(self):
        # Simulate a GET request to the signup view
        response = self.client.get(reverse('signup'))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_user_login_post(self):
        # Create a user
        User.objects.get_or_create(username='testuser1', password='asdBBS123')

        # Simulate a POST request to the login view
        response = self.client.post(reverse('login'), {
            'username': 'testuser1',
            'password': 'asdBBS123',
        })

        # Check if the response redirects to the home page
        self.assertEqual(response.status_code, 200)

    def test_user_login_get(self):
        # Simulate a GET request to the login view
        response = self.client.get(reverse('login'))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

    def test_homepage_authenticated_teacher(self):
        # Create a unique username for the test user
        username = 'testuser_teacher'
        user = User.objects.create_user(username=username, password='12345', isTeacher=True)
        self.client.force_login(user)

        # Make a GET request to the homepage
        response = self.client.get(reverse('homepage'))

        # Check if the 'teacher_courses' variable is present in the response context
        self.assertIn('teacher_courses', response.context)

    def test_homepage_authenticated_student(self):
        user = User.objects.create_user(username='test_student', password='12345')
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertNotIn('teacher_courses', response.context)
        self.assertNotIn('student_courses', response.context)
        self.assertNotIn('enrolled_courses', response.context)

    def test_profile_get(self):
        # Simulate a GET request to the profile view
        response = self.client.get(reverse('profile'))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_post(self):
        # Simulate a POST request to the profile view
        response = self.client.post(reverse('profile'), {
            'bio': 'Updated bio'
        })

        # Check if the response redirects to the homepage
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

        # Check if the profile is updated correctly
        updated_profile = Profile.objects.get(user=self.user_student)
        self.assertEqual(updated_profile.bio, 'Test bio for student')

    def test_create_course_post(self):
        # Simulate a POST request to the create_course view
        response = self.client.post(reverse('create_course'), {
            'name': 'New Course',
            'description': 'Test Description',
            'level': 'beginner',  # Specify the level
        })

        # Check if the response redirects to the homepage
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

        # Check if the course is created in the database
        self.assertTrue(Course.objects.filter(name='New Course').exists())

    def test_delete_course_post(self):
        # Simulate a POST request to the delete_course view
        response = self.client.post(reverse('delete_course', args=[self.course.id]))

        # Check if the response redirects to the homepage
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

        # Check if the course is deleted from the database
        self.assertFalse(Course.objects.filter(id=self.course.id).exists())

    def test_enroll_post(self):
        # Simulate a POST request to the enroll view
        response = self.client.post(reverse('enroll', args=[self.course.id]))

        # Check if the response redirects to the homepage
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

        # Check if the enrollment is created in the database
        self.assertTrue(Enrollment.objects.filter(student=self.user_student, course=self.course).exists())

    def test_view_course_get(self):
        # Simulate a GET request to the view_course view
        response = self.client.get(reverse('view_course', args=[self.course.id]))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Add more assertions to verify the content of the response

    def test_create_material_post(self):
        # Simulate a POST request to the create_material view
        response = self.client.post(reverse('create_material', args=[self.course.id]), {
            'title': 'New Material',
            'description' :'Test',
            'file' : 'test.txt',
        })

        # Check if the response redirects to the view_course page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_course', args=[self.course.id]))

        # Check if the material is created in the database
        self.assertTrue(CourseMaterial.objects.filter(title='New Material', course=self.course).exists())

    def test_delete_material_post(self):
        # Simulate a POST request to the delete_material view
        response = self.client.post(reverse('delete_material', args=[self.material.id]))

        # Check if the response redirects to the view_course page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_course', args=[self.course.id]))

        # Check if the material is deleted from the database
        self.assertFalse(CourseMaterial.objects.filter(id=self.material.id).exists())

    def test_search(self):
        # Simulate a GET request to the search view
        response = self.client.get(reverse('search'), {'query': 'test'})

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Add more assertions to validate the search results

    def test_view_user_teacher(self):
        # Simulate a GET request to view a teacher's profile
        response = self.client.get(reverse('view_user', args=[self.user_teacher.id]))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Add more assertions to validate the content of the response for a teacher profile

    def test_view_user_student(self):
        # Simulate a GET request to view a student's profile
        response = self.client.get(reverse('view_user', args=[self.user_student.id]))

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Add more assertions to validate the content of the response for a student profile

    def test_remove_student(self):
        # Simulate a POST request to remove a student from a course
        response = self.client.post(reverse('remove_student', args=[self.course.id, self.user_student.id]))

        # Check if the response redirects to the view course page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_course', args=[self.course.id]))

        # Check if the student enrollment is deleted from the database
        self.assertFalse(Enrollment.objects.filter(student=self.user_student, course=self.course).exists())

    def test_leave_feedback(self):
        # Simulate a POST request to leave feedback on a course
        response = self.client.post(reverse('leave_feedback', args=[self.course.id]), {'message': 'Test feedback'})

        # Check if the response redirects to the view course page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_course', args=[self.course.id]))



class TestForms(TestCase):
    def test_sign_up_form_valid_data(self):
        form = SignUpForm(data={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'asdBBS123',
            'password2': 'asdBBS123',
            'user_type': 'teacher'
        })

        self.assertTrue(form.is_valid())

    def test_sign_up_form_no_data(self):
        form = SignUpForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 7)  # 7 fields in the form

    def test_profile_form_valid_data(self):
        form = ProfileForm(data={
            'picture': 'test.jpg',
            'bio': 'Test bio'
        })

        self.assertTrue(form.is_valid())

    def test_course_form_valid_data(self):
        form = CourseForm(data={
            'name': 'Test Course',
            'description': 'Test description',
            'level': 'beginner'
        })

        self.assertTrue(form.is_valid())

    def test_material_form_valid_data(self):
        form = MaterialForm(data={
            'title': 'Test Material',
            'description': 'Test description',
            'file': 'test.txt'
        })

        self.assertTrue(form.is_valid())

    def test_search_form_valid_data(self):
        form = SearchForm(data={
            'query': 'test'
        })

        self.assertTrue(form.is_valid())

    def test_feedback_form_valid_data(self):
        form = FeedbackForm(data={
            'rating': 5,
            'comments': 'Test comments'
        })

        self.assertTrue(form.is_valid())

    def test_feedback_form_invalid_data(self):
        form = FeedbackForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # 2 fields in the form


# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Course, CourseMaterial, Feedback

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    user_type=forms.ChoiceField(choices=[('teacher', 'Teacher'), ('student', 'Student')])

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password1', 'password2','user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data.get('user_type')
        if user_type == 'teacher':
            user.isTeacher = True
            user.isStudent = False
        else:
            user.isTeacher = False
            user.isStudent = True
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['picture','bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'picture': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class CourseForm(forms.ModelForm):
    level = forms.ChoiceField(choices=[('beginner', 'Beginner'),
                                    ('intermediate', 'Intermediate'),
                                    ('advanced', 'Advanced')])
    class Meta:
        model = Course
        fields = ['name','description','level']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'description', 'file']


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

class FeedbackForm(forms.ModelForm):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Rating')
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from students.models import Student

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

# Add StudentForm for student portal
class StudentForm(forms.Form):
    first_name   = forms.CharField(label="الاسم الأول", max_length=100,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name    = forms.CharField(label=" اسم العائلة", max_length=100,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    student_id   = forms.CharField(label="رقم الطالب", max_length=50,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    email        = forms.EmailField(label="البريد الإلكتروني",
                                   widget=forms.EmailInput(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(label="تاريخ الميلاد", required=False,
                                   widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))
    level        = forms.CharField(label="المستوى", max_length=50, required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
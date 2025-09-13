from django import forms
from .models import Student, Course, Enrollment, Teacher

# --------- Student: Regular Form (FormOne) ---------
class StudentForm(forms.Form):
    first_name   = forms.CharField(label="الاسم الأول", max_length=100,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name    = forms.CharField(label="اسم العائلة", max_length=100,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    student_id   = forms.CharField(label="رقم الطالب", max_length=50,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    email        = forms.EmailField(label="البريد الإلكتروني",
                                   widget=forms.EmailInput(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(label="تاريخ الميلاد", required=False,
                                   widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))

# --------- Course: Regular Form ---------
class CourseForm(forms.Form):
    code         = forms.CharField(label="رمز المقرر", max_length=50,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    name         = forms.CharField(label="اسم المقرر", max_length=200,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    credit_hours = forms.IntegerField(label="الساعات المعتمدة",
                                      widget=forms.NumberInput(attrs={"class": "form-control"}))

# --------- Enrollment: Regular Form ---------
class EnrollmentForm(forms.Form):
    # نستخدم ModelChoiceField لأن التسجيل مرتبط بطلاب ومقررات
    student  = forms.ModelChoiceField(label="الطالب", queryset=Student.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control"}))
    course   = forms.ModelChoiceField(label="المقرر", queryset=Course.objects.all(),
                                      widget=forms.Select(attrs={"class": "form-control"}))
    semester = forms.CharField(label="الفصل/الترم", max_length=20,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    grade    = forms.ChoiceField(label="التقدير", required=False,
                                 choices=[("A","A"),("B","B"),("C","C"),("IP","IP")],
                                 widget=forms.Select(attrs={"class": "form-control"}))

# --------- Teacher: Regular Form ---------
class TeacherForm(forms.Form):
    first_name = forms.CharField(label="الاسم الأول", max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name  = forms.CharField(label="اسم العائلة", max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    email      = forms.EmailField(label="البريد الإلكتروني",
                                  widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone      = forms.CharField(label="الجوال", max_length=20, required=False,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    department = forms.CharField(label="القسم", max_length=100, required=False,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
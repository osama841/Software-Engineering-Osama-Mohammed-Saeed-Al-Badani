from django import forms
from students.models import Enrollment

class EnrollmentDecisionForm(forms.Form):
    grade = forms.ChoiceField(
        choices=[('', '--- اختر التقدير ---')] + Enrollment.GRADE_CHOICES,
        required=False,
        label='التقدير'
    )

class RejectionReasonForm(forms.Form):
    rejection_reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='سبب الرفض',
        required=True
    )

# Add the StudentForm for the admin panel
from students.models import Student

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
    level        = forms.CharField(label="المستوى", max_length=50, required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
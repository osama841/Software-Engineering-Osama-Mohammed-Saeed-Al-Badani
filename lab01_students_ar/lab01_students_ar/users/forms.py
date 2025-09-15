from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group

class CustomAuthenticationForm(AuthenticationForm):
    user_type = forms.ChoiceField(
        choices=[
            ('', 'اختر نوع المستخدم'),
            ('student', 'طالب'),
            ('teacher', 'أستاذ'),
            ('admin', 'مدير النظام'),
        ],
        label='نوع المستخدم',
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['user_type'].widget.attrs.update({'class': 'form-control'})
        
        # If initial data is provided, set it
        if 'data' in kwargs and kwargs['data']:
            user_type = kwargs['data'].get('user_type', '')
            if user_type:
                self.fields['user_type'].initial = user_type
    
    def confirm_login_allowed(self, user):
        # This method is called after authentication to check if login is allowed
        user_type = self.cleaned_data.get('user_type')
        
        if user_type == 'admin' and not user.is_staff:
            raise forms.ValidationError('ليس لديك صلاحيات مدير النظام')
        elif user_type == 'teacher' and not user.groups.filter(name='Teachers').exists():
            raise forms.ValidationError('ليس لديك صلاحيات أستاذ')
        elif user_type == 'student' and (user.is_staff or user.groups.filter(name='Teachers').exists()):
            raise forms.ValidationError('الرجاء تسجيل الدخول كطالب')
        
        return super().confirm_login_allowed(user)
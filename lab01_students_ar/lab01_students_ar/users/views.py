from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm
from .models import UserProfile
from students.models import Student

def register(request):
    """Register a new student user."""
    if request.method != 'POST':
        # Display blank registration form
        form = UserCreationForm()
    else:
        # Process completed form
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                new_user = form.save()
                
                # Add user to Students group
                try:
                    students_group = Group.objects.get(name='Students')
                    new_user.groups.add(students_group)
                except Group.DoesNotExist:
                    pass
                
                # Create user profile
                UserProfile.objects.create(user=new_user, user_type='student')
                
                # Create student profile
                Student.objects.create(
                    user=new_user,
                    first_name=new_user.username,
                    last_name='',
                    student_id=f'STU{new_user.id:06d}',
                    email=new_user.email or '',
                    approval_status='pending'
                )
                
                # Log the user in and then redirect to complete profile
                login(request, new_user)
                messages.success(request, 'تم إنشاء حسابك بنجاح! يرجى إكمال ملفك الشخصي.')
                return redirect('student_portal:complete_profile')
    
    # Display a blank or invalid form
    context = {
        'form': form,
        'title': 'إنشاء حساب طالب جديد'
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    """Display the user's profile."""
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'user_type': 'student'}
    )
    
    context = {
        'user_profile': user_profile,
    }
    
    # If user is a student, also get their student information
    if user_profile.is_student():
        try:
            student = user_profile.student
            context['student'] = student
            
            # Get student's enrollments
            enrollments = student.enrollments.select_related('course').all()
            context['enrollments'] = enrollments
        except Student.DoesNotExist:
            pass
    
    return render(request, 'users/profile.html', context)

@login_required
def dashboard_redirect(request):
    """Redirect users to their appropriate dashboard based on their role"""
    if request.user.is_staff:
        # Admin user
        return redirect('admin_panel:dashboard')
    elif request.user.groups.filter(name='Teachers').exists():
        # Teacher user
        return redirect('admin_panel:teacher_dashboard')
    else:
        # Student user
        return redirect('student_portal:dashboard')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        # Get the user type from the form
        user_type = form.cleaned_data.get('user_type')
        
        # Authenticate user
        user = form.get_user()
        
        # Check if user type matches the actual user
        if user_type == 'admin' and not user.is_staff:
            form.add_error(None, 'ليس لديك صلاحيات مدير النظام')
            return self.form_invalid(form)
        elif user_type == 'teacher' and not user.groups.filter(name='Teachers').exists():
            form.add_error(None, 'ليس لديك صلاحيات أستاذ')
            return self.form_invalid(form)
        elif user_type == 'student' and (user.is_staff or user.groups.filter(name='Teachers').exists()):
            form.add_error(None, 'الرجاء تسجيل الدخول كطالب')
            return self.form_invalid(form)
        
        # Login the user
        login(self.request, user)
        return super().form_valid(form)
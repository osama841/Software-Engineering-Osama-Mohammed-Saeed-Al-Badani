from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def student_required(view_func):
    """
    Decorator that checks if the user is a student.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Check if user has a profile and is a student
        if hasattr(request.user, 'profile') and request.user.profile.is_student():
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'يجب أن تكون طالبًا للوصول إلى هذه الصفحة.')
            return redirect('home')
    
    return _wrapped_view

def teacher_required(view_func):
    """
    Decorator that checks if the user is a teacher.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Check if user has a profile and is a teacher
        if hasattr(request.user, 'profile') and request.user.profile.is_teacher():
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'يجب أن تكون معلمًا للوصول إلى هذه الصفحة.')
            return redirect('home')
    
    return _wrapped_view

def admin_required(view_func):
    """
    Decorator that checks if the user is an admin.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Check if user is staff/admin
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'يجب أن تكون مشرفًا للوصول إلى هذه الصفحة.')
            return redirect('home')
    
    return _wrapped_view
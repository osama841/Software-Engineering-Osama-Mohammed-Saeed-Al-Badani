from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class AdminAccessMiddleware(MiddlewareMixin):
    """
    Middleware to restrict access to admin site and show appropriate messages
    """
    
    def process_request(self, request):
        # Check if the request is for the admin site
        if request.path.startswith('/admin/'):
            # If user is not authenticated, redirect to login with a message
            if not request.user.is_authenticated:
                messages.error(request, 'يجب تسجيل الدخول للوصول إلى لوحة الإدارة.')
                # Redirect to the main login page
                return redirect('login')
            
            # If user is authenticated but not staff, show a message
            elif not request.user.is_staff:
                messages.error(request, 'أنت مسجل دخول ولكنك غير مخول للوصول إلى لوحة الإدارة. يجب أن يكون لديك صلاحيات المسؤول.')
                # Redirect to home page
                return redirect('home')
                
        return None
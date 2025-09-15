from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from users.views import CustomLoginView

def home_view(request):
    """الصفحة الرئيسية الجديدة"""
    # Always show the home page with appropriate options based on user type
    return render(request, 'home.html')

urlpatterns = [
    # الصفحة الرئيسية الجديدة
    path("", home_view, name='home'),
    
    # لوحة الإدارة Django
    path("admin/", admin.site.urls),

    # تسجيل الدخول والخروج (الواجهة العامة)
    path("login/", CustomLoginView.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path("register/", include("users.urls", namespace="users")),
    
    # Default auth URLs
    path("accounts/", include("django.contrib.auth.urls")),
    
    # بوابة الطالب (بعد تسجيل الدخول)
    path("student/", include("student_portal.urls", namespace="student_portal")),
    
    # لوحة الإدارة المخصصة
    path("admin-panel/", include("admin_panel.urls", namespace="admin_panel")),
    
    # تطبيق الطلاب (للإدارة)
    path("students/", include("students.urls")),

    # تطبيق الملاحظات/التغذية الراجعة
    path("feedback/", include("feedback.urls")),
    path("mailer/", include("mailer.urls", namespace="mailer")),
]
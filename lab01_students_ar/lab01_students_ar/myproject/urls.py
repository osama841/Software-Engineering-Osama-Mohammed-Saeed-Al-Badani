# lab01_students_ar/lab01_students_ar/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # لوحة الإدارة
    path("admin/", admin.site.urls),

    # تطبيق المستخدمين
    path("users/", include("users.urls", namespace="users")),
    
    # Default auth URLs to handle /accounts/login/ redirects
    path("accounts/", include("django.contrib.auth.urls")),
    
    # تطبيق الطلاب
    path("", include("students.urls")),

    # تطبيق الملاحظات/التغذية الراجعة
    path("feedback/", include("feedback.urls")),
    path("mailer/", include("mailer.urls", namespace="mailer")),
]
# students/urls.py
from django.urls import path
from . import views  # يكفي هذا الاستيراد (لا تحتاج from .views import ...)

urlpatterns = [
    # الصفحة الرئيسية للإدارة (تم نقلها للمسار الرئيسي)
    # path('', views.home, name='home'),  # تم إزالتها لتجنب التعارض

    # ========================= الطلاب =========================
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/export/csv/', views.students_export_csv, name='students_export_csv'),
    path('my-profile/', views.student_profile, name='student_profile'),

    # ========================= المقررات =========================
    path('courses/', views.course_list, name='course_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # ========================= التسجيلات =========================
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/create/', views.enrollment_create, name='enrollment_create'),
    path('enrollments/<int:pk>/edit/', views.enrollment_update, name='enrollment_update'),
    path('enrollments/<int:pk>/delete/', views.enrollment_delete, name='enrollment_delete'),

    # ========================= المعلمون =========================
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/edit/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
]
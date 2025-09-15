from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Student management
    path('students/', views.student_list_view, name='student_list'),
    path('students/<int:student_id>/', views.student_detail_view, name='student_detail'),
    path('students/<int:student_id>/approve/', views.approve_student_view, name='approve_student'),
    path('students/<int:student_id>/reject/', views.reject_student_view, name='reject_student'),
    path('students/create/', views.create_student_view, name='create_student'),
    path('students/<int:student_id>/edit/', views.edit_student_view, name='edit_student'),
    path('students/<int:student_id>/delete/', views.delete_student_view, name='delete_student'),
    
    # Teacher management
    path('teachers/', views.teacher_list_view, name='teacher_list'),
    path('teachers/<int:teacher_id>/', views.teacher_detail_view, name='teacher_detail'),
    path('teachers/create/', views.create_teacher_view, name='create_teacher'),
    path('teachers/<int:teacher_id>/edit/', views.edit_teacher_view, name='edit_teacher'),
    path('teachers/<int:teacher_id>/delete/', views.delete_teacher_view, name='delete_teacher'),
    path('teachers/dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    
    # Course management
    path('courses/', views.course_list_view, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('courses/create/', views.create_course_view, name='create_course'),
    path('courses/<int:course_id>/edit/', views.edit_course_view, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course_view, name='delete_course'),
    
    # Enrollment requests
    path('enrollments/', views.enrollment_requests_view, name='enrollment_requests'),
    path('enrollments/<int:enrollment_id>/approve/', views.approve_enrollment_view, name='approve_enrollment'),
    path('enrollments/<int:enrollment_id>/reject/', views.reject_enrollment_view, name='reject_enrollment'),
    
    # Audit log
    path('audit-log/', views.audit_log_view, name='audit_log'),
    
    # Reports and exports
    path('reports/students/export/', views.export_students_csv, name='export_students_csv'),
    path('reports/courses/export/', views.export_courses_csv, name='export_courses_csv'),
    path('reports/enrollments/export/', views.export_enrollments_csv, name='export_enrollments_csv'),
]
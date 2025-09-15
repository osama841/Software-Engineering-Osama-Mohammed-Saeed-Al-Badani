from django.urls import path
from . import views

app_name = 'student_portal'

urlpatterns = [
    # Dashboard (main student page)
    path('', views.student_dashboard_view, name='dashboard'),
    
    # Profile management
    path('profile/complete/', views.complete_profile_view, name='complete_profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/print/', views.print_profile_view, name='print_profile'),
    
    # Enrollment requests
    path('enrollments/request/', views.request_enrollment_view, name='request_enrollment'),
    path('enrollments/', views.student_enrollments_view, name='student_enrollments'),
]
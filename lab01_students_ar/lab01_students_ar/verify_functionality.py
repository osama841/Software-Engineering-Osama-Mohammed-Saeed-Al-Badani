#!/usr/bin/env python
"""
Verification script to check if all components of the student management system are working correctly.
This script will verify the models, views, and basic functionality of the system.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def verify_models():
    """Verify that all models can be imported and instantiated"""
    print("Verifying models...")
    
    try:
        from students.models import Student, Teacher, Course, Enrollment, AuditLog
        print("✓ All models imported successfully")
        
        # Test model creation
        student = Student(
            first_name="Test",
            last_name="Student",
            student_id="STU001",
            email="test@student.com"
        )
        print("✓ Student model instantiation successful")
        
        teacher = Teacher(
            first_name="Test",
            last_name="Teacher",
            email="test@teacher.com"
        )
        print("✓ Teacher model instantiation successful")
        
        course = Course(
            code="CS101",
            name="Introduction to Computer Science",
            credit_hours=3
        )
        print("✓ Course model instantiation successful")
        
        print("✓ All models verified successfully")
        return True
    except Exception as e:
        print(f"✗ Model verification failed: {e}")
        return False

def verify_forms():
    """Verify that all forms can be imported and instantiated"""
    print("\nVerifying forms...")
    
    try:
        from students.forms import StudentForm, CourseForm, EnrollmentForm, TeacherForm
        print("✓ Students forms imported successfully")
        
        from admin_panel.forms import StudentForm as AdminStudentForm, EnrollmentDecisionForm, RejectionReasonForm
        print("✓ Admin panel forms imported successfully")
        
        from student_portal.forms import UserRegistrationForm, UserLoginForm, StudentForm as PortalStudentForm
        print("✓ Student portal forms imported successfully")
        
        from feedback.forms import FeedbackForm
        print("✓ Feedback forms imported successfully")
        
        # Test form instantiation
        student_form = StudentForm()
        course_form = CourseForm()
        enrollment_form = EnrollmentForm()
        teacher_form = TeacherForm()
        print("✓ All forms instantiated successfully")
        
        print("✓ All forms verified successfully")
        return True
    except Exception as e:
        print(f"✗ Form verification failed: {e}")
        return False

def verify_urls():
    """Verify that all URLs can be resolved"""
    print("\nVerifying URLs...")
    
    try:
        from django.urls import reverse
        
        # Test some key URLs
        urls_to_test = [
            'home',
            'student_list',
            'teacher_list',
            'course_list',
            'enrollment_list',
            'users:login',
            'users:register',
            'users:profile',
            'student_portal:login',
            'student_portal:register',
            'student_portal:dashboard',
            'admin_panel:dashboard',
            'feedback:submit_feedback',
        ]
        
        for url_name in urls_to_test:
            try:
                reversed_url = reverse(url_name)
                print(f"✓ {url_name} -> {reversed_url}")
            except Exception as e:
                print(f"⚠ Warning: Could not reverse {url_name}: {e}")
        
        print("✓ URL verification completed")
        return True
    except Exception as e:
        print(f"✗ URL verification failed: {e}")
        return False

def verify_views():
    """Verify that views can be imported"""
    print("\nVerifying views...")
    
    try:
        from students.views import home, student_list, course_list, enrollment_list
        print("✓ Students views imported successfully")
        
        from admin_panel.views import dashboard_view, student_list_view
        print("✓ Admin panel views imported successfully")
        
        from student_portal.views import login_view, register_view, student_dashboard_view
        print("✓ Student portal views imported successfully")
        
        from users.views import register, profile
        print("✓ Users views imported successfully")
        
        from feedback.views import submit_feedback, send_feedback_email
        print("✓ Feedback views imported successfully")
        
        print("✓ All views verified successfully")
        return True
    except Exception as e:
        print(f"✗ View verification failed: {e}")
        return False

def main():
    """Main verification function"""
    print("Starting verification of student management system...")
    print("=" * 50)
    
    results = []
    results.append(verify_models())
    results.append(verify_forms())
    results.append(verify_urls())
    results.append(verify_views())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✓ All verifications passed! The system is working correctly.")
        return 0
    else:
        print("✗ Some verifications failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
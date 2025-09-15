from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from students.models import Student, Teacher, Course

class AdminPanelViewTest(TestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Create teacher user
        self.teacher_user = User.objects.create_user(
            username='teacher',
            password='teacherpass123'
        )
        
        # Create teacher group
        self.teacher_group, created = Group.objects.get_or_create(name='Teachers')
        self.teacher_user.groups.add(self.teacher_group)
        
        # Create teacher profile
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            first_name='Test',
            last_name='Teacher',
            email='teacher@example.com'
        )
        
        # Create student
        self.student = Student.objects.create(
            first_name='Test',
            last_name='Student',
            student_id='STU001',
            email='test@student.com',
            approval_status='pending'
        )
        
        # Create course
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            credit_hours=3,
            teacher=self.teacher
        )
    
    def test_admin_can_access_admin_dashboard(self):
        """Test that admin can access admin dashboard"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_panel:dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_teacher_can_access_teacher_dashboard(self):
        """Test that teacher can access teacher dashboard"""
        self.client.login(username='teacher', password='teacherpass123')
        response = self.client.get(reverse('admin_panel:teacher_dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_access_student_list(self):
        """Test that admin can access student list"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_panel:student_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_access_teacher_list(self):
        """Test that admin can access teacher list"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_panel:teacher_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_access_course_list(self):
        """Test that admin can access course list"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_panel:course_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_user_cannot_access_admin_dashboard(self):
        """Test that unauthenticated user cannot access admin dashboard"""
        response = self.client.get(reverse('admin_panel:dashboard'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
    
    def test_teacher_cannot_access_admin_student_list(self):
        """Test that teacher cannot access admin student list"""
        self.client.login(username='teacher', password='teacherpass123')
        response = self.client.get(reverse('admin_panel:student_list'))
        # Should redirect or show permission denied
        self.assertEqual(response.status_code, 302)
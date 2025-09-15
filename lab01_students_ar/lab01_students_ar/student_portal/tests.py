from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from students.models import Student

class StudentPortalViewTest(TestCase):
    def setUp(self):
        # Create student user
        self.student_user = User.objects.create_user(
            username='teststudent',
            password='testpass123',
            email='test@student.com'
        )
        
        # Create student group
        self.student_group, created = Group.objects.get_or_create(name='Students')
        self.student_user.groups.add(self.student_group)
        
        # Create student profile
        self.student = Student.objects.create(
            user=self.student_user,
            first_name='Test',
            last_name='Student',
            student_id='STU001',
            email='test@student.com',
            approval_status='approved'
        )
        
        # Create another user for login testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_student_can_access_login_page(self):
        """Test that users can access the login page"""
        response = self.client.get(reverse('student_portal:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_can_access_register_page(self):
        """Test that users can access the registration page"""
        response = self.client.get(reverse('student_portal:register'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_can_login(self):
        """Test that student can login"""
        response = self.client.post(reverse('student_portal:login'), {
            'username': 'teststudent',
            'password': 'testpass123'
        })
        # Should redirect to dashboard
        self.assertEqual(response.status_code, 302)
    
    def test_student_can_access_dashboard_when_logged_in(self):
        """Test that logged in student can access dashboard"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('student_portal:dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_can_logout(self):
        """Test that student can logout"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('logout'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
    
    def test_unauthenticated_user_cannot_access_dashboard(self):
        """Test that unauthenticated user cannot access dashboard"""
        response = self.client.get(reverse('student_portal:dashboard'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
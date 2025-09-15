from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from users.models import UserProfile
from students.models import Student

class UsersViewTest(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create student group
        self.student_group, created = Group.objects.get_or_create(name='Students')
    
    def test_user_can_register(self):
        """Test that user can register"""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        
        # Test registration post
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        # Should redirect to home page
        self.assertEqual(response.status_code, 302)
        
        # Check that user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_user_can_login(self):
        """Test that user can login"""
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Should redirect to home page
        self.assertEqual(response.status_code, 302)
    
    def test_user_can_access_profile_when_logged_in(self):
        """Test that logged in user can access profile"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_can_logout(self):
        """Test that user can logout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('users:logout'))
        # Should redirect to home page
        self.assertEqual(response.status_code, 302)
    
    def test_unauthenticated_user_cannot_access_profile(self):
        """Test that unauthenticated user cannot access profile"""
        response = self.client.get(reverse('users:profile'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)

class UsersModelTest(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create student
        self.student = Student.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            student_id='STU001',
            email='test@example.com'
        )
        
        # Create user profile
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            user_type='student',
            student=self.student
        )
    
    def test_user_profile_creation(self):
        """Test that user profile is created correctly"""
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.user_type, 'student')
        self.assertEqual(self.user_profile.student, self.student)
    
    def test_user_profile_str_representation(self):
        """Test user profile string representation"""
        self.assertEqual(str(self.user_profile), f"{self.user.username} - طالب")
    
    def test_user_profile_is_student(self):
        """Test is_student method"""
        self.assertTrue(self.user_profile.is_student())
    
    def test_user_profile_is_teacher(self):
        """Test is_teacher method"""
        self.assertFalse(self.user_profile.is_teacher())
    
    def test_user_profile_is_admin(self):
        """Test is_admin method"""
        self.assertFalse(self.user_profile.is_admin())
        
        # Test with staff user
        staff_user = User.objects.create_user(
            username='staffuser',
            password='testpass123',
            is_staff=True
        )
        staff_profile = UserProfile.objects.create(
            user=staff_user,
            user_type='admin'
        )
        self.assertTrue(staff_profile.is_admin())
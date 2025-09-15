from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Student, Teacher, Course, Enrollment

class StudentModelTest(TestCase):
    def setUp(self):
        # Create student user
        self.student_user = User.objects.create_user(
            username='teststudent',
            password='testpass123'
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
        
        # Create teacher
        self.teacher_user = User.objects.create_user(
            username='testteacher',
            password='testpass123'
        )
        
        # Create teacher group
        self.teacher_group, created = Group.objects.get_or_create(name='Teachers')
        self.teacher_user.groups.add(self.teacher_group)
        
        # Create teacher profile
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            first_name='Test',
            last_name='Teacher',
            email='test@teacher.com'
        )
        
        # Create course
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            credit_hours=3,
            teacher=self.teacher
        )
        
        # Create enrollment
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            semester='2025S1',
            request_status='approved'
        )
    
    def test_student_creation(self):
        """Test that student is created correctly"""
        self.assertEqual(self.student.first_name, 'Test')
        self.assertEqual(self.student.last_name, 'Student')
        self.assertEqual(self.student.student_id, 'STU001')
        self.assertEqual(self.student.email, 'test@student.com')
        self.assertEqual(self.student.approval_status, 'approved')
    
    def test_student_str_representation(self):
        """Test student string representation"""
        self.assertEqual(str(self.student), 'Test Student (STU001)')
    
    def test_teacher_creation(self):
        """Test that teacher is created correctly"""
        self.assertEqual(self.teacher.first_name, 'Test')
        self.assertEqual(self.teacher.last_name, 'Teacher')
        self.assertEqual(self.teacher.email, 'test@teacher.com')
    
    def test_course_creation(self):
        """Test that course is created correctly"""
        self.assertEqual(self.course.code, 'CS101')
        self.assertEqual(self.course.name, 'Introduction to Computer Science')
        self.assertEqual(self.course.credit_hours, 3)
        self.assertEqual(self.course.teacher, self.teacher)
    
    def test_enrollment_creation(self):
        """Test that enrollment is created correctly"""
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.course, self.course)
        self.assertEqual(self.enrollment.semester, '2025S1')
        self.assertEqual(self.enrollment.request_status, 'approved')

class StudentViewTest(TestCase):
    def setUp(self):
        # Create student user
        self.student_user = User.objects.create_user(
            username='teststudent',
            password='testpass123'
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
        
        # Create teacher
        self.teacher_user = User.objects.create_user(
            username='testteacher',
            password='testpass123'
        )
        
        # Create teacher group
        self.teacher_group, created = Group.objects.get_or_create(name='Teachers')
        self.teacher_user.groups.add(self.teacher_group)
        
        # Create teacher profile
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            first_name='Test',
            last_name='Teacher',
            email='test@teacher.com'
        )
        
        # Create course
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            credit_hours=3,
            teacher=self.teacher
        )
    
    def test_student_can_access_homepage(self):
        """Test that student can access homepage"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_can_access_course_list(self):
        """Test that student can access course list"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_can_access_enrollment_list(self):
        """Test that student can access enrollment list"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('enrollment_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_student_can_access_profile(self):
        """Test that student can access their profile"""
        self.client.login(username='teststudent', password='testpass123')
        response = self.client.get(reverse('student_profile'))
        self.assertEqual(response.status_code, 200)

class AdminViewTest(TestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Create student
        self.student = Student.objects.create(
            first_name='Test',
            last_name='Student',
            student_id='STU001',
            email='test@student.com',
            approval_status='pending'
        )
        
        # Create teacher
        self.teacher = Teacher.objects.create(
            first_name='Test',
            last_name='Teacher',
            email='test@teacher.com'
        )
        
        # Create course
        self.course = Course.objects.create(
            code='CS101',
            name='Introduction to Computer Science',
            credit_hours=3,
            teacher=self.teacher
        )
    
    def test_admin_can_access_student_list(self):
        """Test that admin can access student list"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_access_teacher_list(self):
        """Test that admin can access teacher list"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('teacher_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_access_course_list(self):
        """Test that admin can access course list"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_can_access_enrollment_list(self):
        """Test that admin can access enrollment list"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('enrollment_list'))
        self.assertEqual(response.status_code, 200)
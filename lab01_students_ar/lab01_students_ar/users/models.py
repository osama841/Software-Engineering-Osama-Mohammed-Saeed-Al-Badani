from django.db import models
from django.contrib.auth.models import User
from students.models import Student, Teacher

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'طالب'),
        ('teacher', 'معلم'),
        ('admin', 'مدير'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField('نوع المستخدم', max_length=10, choices=USER_TYPE_CHOICES, default='student')
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='user_profile')
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='user_profile')
    
    class Meta:
        verbose_name = 'ملف المستخدم'
        verbose_name_plural = 'ملفات المستخدمين'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    
    def is_student(self):
        return self.user_type == 'student' and self.student is not None
    
    def is_teacher(self):
        return self.user_type == 'teacher' and self.teacher is not None
    
    def is_admin(self):
        return self.user_type == 'admin' or self.user.is_staff

from django.db import models

class Student(models.Model):
    first_name = models.CharField('الاسم الأول', max_length=50)
    last_name = models.CharField('اسم العائلة', max_length=50)
    student_id = models.CharField('رقم الطالب', max_length=20, unique=True)
    email = models.EmailField('البريد الإلكتروني', unique=True)
    date_of_birth = models.DateField('تاريخ الميلاد', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'طالب'
        verbose_name_plural = 'الطلاب'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Course(models.Model):
    code = models.CharField('كود المقرر', max_length=10, unique=True)
    name = models.CharField('اسم المقرر', max_length=100)
    credit_hours = models.PositiveSmallIntegerField('الساعات', default=3)

    class Meta:
        ordering = ['code']
        verbose_name = 'مقرر'
        verbose_name_plural = 'المقررات'

    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'), ('IP', 'قيد الإنجاز')
    ]
    student = models.ForeignKey(Student, verbose_name='الطالب', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, verbose_name='المقرر', on_delete=models.CASCADE, related_name='enrollments')
    semester = models.CharField('الفصل', max_length=20)  # e.g., 2025S1
    grade = models.CharField('التقدير', max_length=2, choices=GRADE_CHOICES, default='IP')

    class Meta:
        unique_together = ('student', 'course', 'semester')
        ordering = ['-semester']
        verbose_name = 'تسجيل'
        verbose_name_plural = 'التسجيلات'

    def __str__(self):
        return f"{self.student} -> {self.course} ({self.semester})"


class Teacher(models.Model):
    first_name = models.CharField("الاسم الأول", max_length=100)
    last_name  = models.CharField("اسم العائلة", max_length=100)
    email      = models.EmailField("البريد الإلكتروني", unique=True)
    phone      = models.CharField("الجوال", max_length=20, blank=True)
    department = models.CharField("القسم", max_length=100, blank=True)

    class Meta:
        verbose_name = "معلم"
        verbose_name_plural = "المعلمون"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Student(models.Model):
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'قيد المراجعة'),
        ('approved', 'معتمد'),
        ('rejected', 'مرفوض'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    first_name = models.CharField('الاسم الأول', max_length=50)
    last_name = models.CharField('اسم العائلة', max_length=50)
    student_id = models.CharField('رقم الطالب', max_length=20, unique=True)
    email = models.EmailField('البريد الإلكتروني', unique=True)
    date_of_birth = models.DateField('تاريخ الميلاد', null=True, blank=True)
    level = models.CharField('المستوى', max_length=50, blank=True)  # e.g., "السنة الأولى", "السنة الثانية"
    approval_status = models.CharField('حالة الاعتماد', max_length=10, choices=APPROVAL_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('تاريخ الإنشاء', default=timezone.now)
    updated_at = models.DateTimeField('تاريخ آخر تحديث', default=timezone.now)
    approved_at = models.DateTimeField('تاريخ الاعتماد', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'طالب'
        verbose_name_plural = 'الطلاب'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def is_approved(self):
        return self.approval_status == 'approved'

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', null=True, blank=True)
    first_name = models.CharField("الاسم الأول", max_length=100)
    last_name = models.CharField("اسم العائلة", max_length=100)
    email = models.EmailField("البريد الإلكتروني", unique=True)
    phone = models.CharField("الجوال", max_length=20, blank=True)
    department = models.CharField("القسم", max_length=100, blank=True)
    created_at = models.DateTimeField('تاريخ الإنشاء', default=timezone.now)
    updated_at = models.DateTimeField('تاريخ آخر تحديث', default=timezone.now)

    class Meta:
        verbose_name = "معلم"
        verbose_name_plural = "المعلمون"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Course(models.Model):
    code = models.CharField('كود المقرر', max_length=10, unique=True)
    name = models.CharField('اسم المقرر', max_length=100)
    credit_hours = models.PositiveSmallIntegerField('الساعات', default=3)
    teacher = models.ForeignKey(Teacher, verbose_name='المعلم المسؤول', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    created_at = models.DateTimeField('تاريخ الإنشاء', default=timezone.now)
    updated_at = models.DateTimeField('تاريخ آخر تحديث', default=timezone.now)

    class Meta:
        ordering = ['code']
        verbose_name = 'مقرر'
        verbose_name_plural = 'المقررات'

    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    REQUEST_STATUS_CHOICES = [
        ('requested', 'مطلوب'),
        ('approved', 'معتمد'),
        ('rejected', 'مرفوض'),
    ]
    
    GRADE_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'), ('IP', 'قيد الإنجاز')
    ]
    
    student = models.ForeignKey(Student, verbose_name='الطالب', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, verbose_name='المقرر', on_delete=models.CASCADE, related_name='enrollments')
    semester = models.CharField('الفصل', max_length=20)  # e.g., 2025S1
    grade = models.CharField('التقدير', max_length=2, choices=GRADE_CHOICES, default='IP')
    request_status = models.CharField('حالة الطلب', max_length=10, choices=REQUEST_STATUS_CHOICES, default='requested')
    request_date = models.DateTimeField('تاريخ الطلب', default=timezone.now)
    approval_date = models.DateTimeField('تاريخ الاعتماد', null=True, blank=True)
    approved_by = models.ForeignKey(User, verbose_name='معتمد بواسطة', on_delete=models.SET_NULL, null=True, blank=True)
    rejection_reason = models.TextField('سبب الرفض', blank=True)

    class Meta:
        unique_together = ('student', 'course', 'semester')
        ordering = ['-request_date']
        verbose_name = 'تسجيل'
        verbose_name_plural = 'التسجيلات'

    def __str__(self):
        return f"{self.student} -> {self.course} ({self.semester})"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'إنشاء'),
        ('update', 'تحديث'),
        ('delete', 'حذف'),
        ('approve', 'اعتماد'),
        ('reject', 'رفض'),
    ]
    
    user = models.ForeignKey(User, verbose_name='المستخدم', on_delete=models.CASCADE)
    action = models.CharField('الإجراء', max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField('اسم النموذج', max_length=50)
    object_id = models.PositiveIntegerField('معرف العنصر')
    description = models.TextField('الوصف')
    timestamp = models.DateTimeField('الطابع الزمني', default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'سجل تدقيق'
        verbose_name_plural = 'سجلات التدقيق'

    def __str__(self):
        return f"{self.user} - {self.action} {self.model_name} ({self.timestamp})"
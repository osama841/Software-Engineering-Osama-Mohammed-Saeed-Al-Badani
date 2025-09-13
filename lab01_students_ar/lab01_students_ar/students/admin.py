from django.contrib import admin
from .models import Student, Course, Enrollment, Teacher

# Register models with the default admin site
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credit_hours')
    search_fields = ('code', 'name')
    list_filter = ('credit_hours',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'grade')
    list_filter = ('semester', 'grade', 'course')
    search_fields = ('student__student_id', 'student__first_name', 'student__last_name', 'course__code', 'course__name')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "department")
    search_fields = ("first_name", "last_name", "email", "department")

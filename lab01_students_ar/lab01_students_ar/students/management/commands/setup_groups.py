from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from students.models import Student, Teacher, Course, Enrollment, AuditLog

class Command(BaseCommand):
    help = 'Set up user groups and permissions'

    def handle(self, *args, **options):
        # Create groups
        students_group, created = Group.objects.get_or_create(name='Students')
        staff_group, created = Group.objects.get_or_create(name='Staff')
        teachers_group, created = Group.objects.get_or_create(name='Teachers')

        # Get content types
        student_content_type = ContentType.objects.get_for_model(Student)
        teacher_content_type = ContentType.objects.get_for_model(Teacher)
        course_content_type = ContentType.objects.get_for_model(Course)
        enrollment_content_type = ContentType.objects.get_for_model(Enrollment)
        auditlog_content_type = ContentType.objects.get_for_model(AuditLog)

        # Permissions for Students group
        # Students can only view their own profile and enrollments
        students_group.permissions.clear()

        # Permissions for Staff group
        # Staff can manage all models
        staff_permissions = Permission.objects.filter(
            content_type__in=[
                student_content_type,
                teacher_content_type,
                course_content_type,
                enrollment_content_type,
                auditlog_content_type
            ]
        )
        staff_group.permissions.set(staff_permissions)

        # Permissions for Teachers group
        # Teachers can only view courses and enrollments related to them
        teachers_group.permissions.clear()

        self.stdout.write(
            self.style.SUCCESS('Successfully set up user groups and permissions')
        )
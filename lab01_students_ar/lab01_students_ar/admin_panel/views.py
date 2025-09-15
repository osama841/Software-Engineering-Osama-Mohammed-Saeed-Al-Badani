from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils import timezone
import csv
from students.models import Student, Teacher, Course, Enrollment, AuditLog
from students.forms import TeacherForm, CourseForm, EnrollmentForm
from .forms import EnrollmentDecisionForm, RejectionReasonForm, StudentForm

def is_staff_member(user):
    """Check if user is staff member"""
    return user.is_staff

@login_required
@user_passes_test(is_staff_member)
def dashboard_view(request):
    """Admin panel dashboard"""
    # Get statistics
    pending_students = Student.objects.filter(approval_status='pending').count()
    pending_enrollments = Enrollment.objects.filter(request_status='requested').count()
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    
    # Get recent audit logs
    recent_audit_logs = AuditLog.objects.select_related('user').order_by('-timestamp')[:10]
    
    context = {
        'pending_students': pending_students,
        'pending_enrollments': pending_enrollments,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'recent_audit_logs': recent_audit_logs,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@user_passes_test(is_staff_member)
def student_list_view(request):
    """List all students with search and filters"""
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    
    students = Student.objects.all()
    
    # Apply search filter
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(email__icontains=query)
        )
    
    # Apply status filter
    if status:
        students = students.filter(approval_status=status)
    
    # Order by last name
    students = students.order_by('last_name')
    
    context = {
        'students': students,
        'query': query,
        'status': status,
    }
    return render(request, 'admin_panel/students/list.html', context)

@login_required
@user_passes_test(is_staff_member)
def student_detail_view(request, student_id):
    """View student details"""
    student = get_object_or_404(Student, id=student_id)
    enrollments = Enrollment.objects.filter(student=student).select_related('course', 'course__teacher')
    
    context = {
        'student': student,
        'enrollments': enrollments,
    }
    return render(request, 'admin_panel/students/detail.html', context)

@login_required
@user_passes_test(is_staff_member)
def approve_student_view(request, student_id):
    """Approve student profile"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.approval_status = 'approved'
        student.approved_at = timezone.now()
        student.save()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='approve',
            model_name='Student',
            object_id=student.id,
            description=f'تم اعتماد الطالب {student.first_name} {student.last_name}'
        )
        
        messages.success(request, f'تم اعتماد الطالب {student.first_name} {student.last_name} بنجاح.')
        return redirect('admin_panel:student_detail', student_id=student.id)
    
    context = {
        'student': student,
    }
    return render(request, 'admin_panel/students/approve_confirm.html', context)

@login_required
@user_passes_test(is_staff_member)
def reject_student_view(request, student_id):
    """Reject student profile"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = RejectionReasonForm(request.POST)
        if form.is_valid():
            rejection_reason = form.cleaned_data['rejection_reason']
            student.approval_status = 'rejected'
            student.save()
            
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='reject',
                model_name='Student',
                object_id=student.id,
                description=f'تم رفض الطالب {student.first_name} {student.last_name} - السبب: {rejection_reason}'
            )
            
            messages.success(request, f'تم رفض الطالب {student.first_name} {student.last_name} بنجاح.')
            return redirect('admin_panel:student_detail', student_id=student.id)
    else:
        form = RejectionReasonForm()
    
    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'admin_panel/students/reject_form.html', context)

@login_required
@user_passes_test(is_staff_member)
def create_student_view(request):
    """Create a new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = Student.objects.create(**form.cleaned_data)
            
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='create',
                model_name='Student',
                object_id=student.id,
                description=f'تم إنشاء الطالب {student.first_name} {student.last_name}'
            )
            
            messages.success(request, f'تم إنشاء الطالب {student.first_name} {student.last_name} بنجاح.')
            return redirect('admin_panel:student_list')
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'title': 'إنشاء طالب جديد',
    }
    return render(request, 'admin_panel/students/form.html', context)

@login_required
@user_passes_test(is_staff_member)
def edit_student_view(request, student_id):
    """Edit student information"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            student.first_name = cd["first_name"]
            student.last_name = cd["last_name"]
            student.student_id = cd["student_id"]
            student.email = cd["email"]
            student.date_of_birth = cd.get("date_of_birth")
            student.level = cd.get("level", "")
            student.save()
            
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='update',
                model_name='Student',
                object_id=student.id,
                description=f'تم تحديث معلومات الطالب {student.first_name} {student.last_name}'
            )
            
            messages.success(request, f'تم تحديث معلومات الطالب {student.first_name} {student.last_name} بنجاح.')
            return redirect('admin_panel:student_detail', student_id=student.id)
    else:
        form = StudentForm(initial={
            "first_name": student.first_name,
            "last_name": student.last_name,
            "student_id": student.student_id,
            "email": student.email,
            "date_of_birth": student.date_of_birth,
            "level": student.level,
        })
    
    context = {
        'form': form,
        'student': student,
        'title': 'تعديل معلومات الطالب',
    }
    return render(request, 'admin_panel/students/form.html', context)

@login_required
@user_passes_test(is_staff_member)
def delete_student_view(request, student_id):
    """Delete student"""
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student_name = f'{student.first_name} {student.last_name}'
        student.delete()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='delete',
            model_name='Student',
            object_id=student_id,
            description=f'تم حذف الطالب {student_name}'
        )
        
        messages.success(request, f'تم حذف الطالب {student_name} بنجاح.')
        return redirect('admin_panel:student_list')
    
    context = {
        'student': student,
    }
    return render(request, 'admin_panel/students/delete_confirm.html', context)

@login_required
@user_passes_test(is_staff_member)
def teacher_list_view(request):
    """List all teachers with search"""
    query = request.GET.get('q', '')
    
    teachers = Teacher.objects.all()
    
    # Apply search filter
    if query:
        teachers = teachers.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(department__icontains=query)
        )
    
    # Order by last name
    teachers = teachers.order_by('last_name')
    
    context = {
        'teachers': teachers,
        'query': query,
    }
    return render(request, 'admin_panel/teachers/list.html', context)

@login_required
@user_passes_test(is_staff_member)
def teacher_detail_view(request, teacher_id):
    """View teacher details"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    courses = Course.objects.filter(teacher=teacher)
    
    context = {
        'teacher': teacher,
        'courses': courses,
    }
    return render(request, 'admin_panel/teachers/detail.html', context)

@login_required
@user_passes_test(is_staff_member)
def create_teacher_view(request):
    """Create a new teacher"""
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='create',
                model_name='Teacher',
                object_id=teacher.id,
                description=f'تم إنشاء المعلم {teacher.first_name} {teacher.last_name}'
            )
            
            messages.success(request, f'تم إنشاء المعلم {teacher.first_name} {teacher.last_name} بنجاح.')
            return redirect('admin_panel:teacher_list')
    else:
        form = TeacherForm()
    
    context = {
        'form': form,
        'title': 'إنشاء معلم جديد',
    }
    return render(request, 'admin_panel/teachers/form.html', context)

@login_required
@user_passes_test(is_staff_member)
def edit_teacher_view(request, teacher_id):
    """Edit teacher information"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            teacher = form.save()
            
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='update',
                model_name='Teacher',
                object_id=teacher.id,
                description=f'تم تحديث معلومات المعلم {teacher.first_name} {teacher.last_name}'
            )
            
            messages.success(request, f'تم تحديث معلومات المعلم {teacher.first_name} {teacher.last_name} بنجاح.')
            return redirect('admin_panel:teacher_detail', teacher_id=teacher.id)
    else:
        form = TeacherForm(instance=teacher)
    
    context = {
        'form': form,
        'teacher': teacher,
        'title': 'تعديل معلومات المعلم',
    }
    return render(request, 'admin_panel/teachers/form.html', context)

@login_required
@user_passes_test(is_staff_member)
def delete_teacher_view(request, teacher_id):
    """Delete teacher"""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        teacher_name = f'{teacher.first_name} {teacher.last_name}'
        teacher.delete()
        
        # Log the action
        AuditLog.objects.create(
                user=request.user,
                action='delete',
                model_name='Teacher',
                object_id=teacher_id,
                description=f'تم حذف المعلم {teacher_name}'
            )
        
        messages.success(request, f'تم حذف المعلم {teacher_name} بنجاح.')
        return redirect('admin_panel:teacher_list')
    
    context = {
        'teacher': teacher,
    }
    return render(request, 'admin_panel/teachers/delete_confirm.html', context)

@login_required
@user_passes_test(is_staff_member)
def course_list_view(request):
    """List all courses with search"""
    query = request.GET.get('q', '')
    
    courses = Course.objects.all()
    
    # Apply search filter
    if query:
        courses = courses.filter(
            Q(code__icontains=query) |
            Q(name__icontains=query)
        )
    
    # Order by code
    courses = courses.order_by('code')
    
    context = {
        'courses': courses,
        'query': query,
    }
    return render(request, 'admin_panel/courses/list.html', context)

@login_required
@user_passes_test(is_staff_member)
def course_detail_view(request, course_id):
    """View course details"""
    course = get_object_or_404(Course, id=course_id)
    enrollments = Enrollment.objects.filter(course=course).select_related('student')
    
    context = {
        'course': course,
        'enrollments': enrollments,
    }
    return render(request, 'admin_panel/courses/detail.html', context)

@login_required
@user_passes_test(is_staff_member)
def create_course_view(request):
    """Create a new course"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='create',
                model_name='Course',
                object_id=course.id,
                description=f'تم إنشاء المقرر {course.code} - {course.name}'
            )
            
            messages.success(request, f'تم إنشاء المقرر {course.code} - {course.name} بنجاح.')
            return redirect('admin_panel:course_list')
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'title': 'إنشاء مقرر جديد',
    }
    return render(request, 'admin_panel/courses/form.html', context)

@login_required
@user_passes_test(is_staff_member)
def edit_course_view(request, course_id):
    """Edit course information"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='update',
                model_name='Course',
                object_id=course.id,
                description=f'تم تحديث معلومات المقرر {course.code} - {course.name}'
            )
            
            messages.success(request, f'تم تحديث معلومات المقرر {course.code} - {course.name} بنجاح.')
            return redirect('admin_panel:course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'course': course,
        'title': 'تعديل معلومات المقرر',
    }
    return render(request, 'admin_panel/courses/form.html', context)

@login_required
@user_passes_test(is_staff_member)
def delete_course_view(request, course_id):
    """Delete course"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        course_code = course.code
        course_name = course.name
        course.delete()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='delete',
            model_name='Course',
            object_id=course_id,
            description=f'تم حذف المقرر {course_code} - {course_name}'
        )
        
        messages.success(request, f'تم حذف المقرر {course_code} - {course_name} بنجاح.')
        return redirect('admin_panel:course_list')
    
    context = {
        'course': course,
    }
    return render(request, 'admin_panel/courses/delete_confirm.html', context)

@login_required
@user_passes_test(is_staff_member)
def enrollment_requests_view(request):
    """List all enrollment requests"""
    status = request.GET.get('status', 'requested')
    
    enrollments = Enrollment.objects.filter(request_status=status).select_related(
        'student', 'course', 'course__teacher'
    )
    
    # Order by request date
    enrollments = enrollments.order_by('-request_date')
    
    context = {
        'enrollments': enrollments,
        'status': status,
    }
    return render(request, 'admin_panel/enrollments/list.html', context)

@login_required
@user_passes_test(is_staff_member)
def approve_enrollment_view(request, enrollment_id):
    """Approve enrollment request"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if request.method == 'POST':
        form = EnrollmentDecisionForm(request.POST)
        if form.is_valid():
            enrollment.request_status = 'approved'
            enrollment.approval_date = timezone.now()
            enrollment.approved_by = request.user
            enrollment.save()
            
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='approve',
                model_name='Enrollment',
                object_id=enrollment.id,
                description=f'تم اعتماد تسجيل الطالب {enrollment.student.first_name} {enrollment.student.last_name} في المقرر {enrollment.course.code} - {enrollment.course.name}'
            )
            
            messages.success(request, f'تم اعتماد تسجيل الطالب {enrollment.student.first_name} {enrollment.student.last_name} في المقرر {enrollment.course.code} - {enrollment.course.name} بنجاح.')
            return redirect('admin_panel:enrollment_requests')
    else:
        form = EnrollmentDecisionForm()
    
    context = {
        'enrollment': enrollment,
        'form': form,
    }
    return render(request, 'admin_panel/enrollments/approve_form.html', context)

@login_required
@user_passes_test(is_staff_member)
def reject_enrollment_view(request, enrollment_id):
    """Reject enrollment request"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if request.method == 'POST':
        form = RejectionReasonForm(request.POST)
        if form.is_valid():
            rejection_reason = form.cleaned_data['rejection_reason']
            enrollment.request_status = 'rejected'
            enrollment.approval_date = timezone.now()
            enrollment.approved_by = request.user
            enrollment.rejection_reason = rejection_reason
            enrollment.save()
            
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='reject',
                model_name='Enrollment',
                object_id=enrollment.id,
                description=f'تم رفض تسجيل الطالب {enrollment.student.first_name} {enrollment.student.last_name} في المقرر {enrollment.course.code} - {enrollment.course.name} - السبب: {rejection_reason}'
            )
            
            messages.success(request, f'تم رفض تسجيل الطالب {enrollment.student.first_name} {enrollment.student.last_name} في المقرر {enrollment.course.code} - {enrollment.course.name} بنجاح.')
            return redirect('admin_panel:enrollment_requests')
    else:
        form = RejectionReasonForm()
    
    context = {
        'enrollment': enrollment,
        'form': form,
    }
    return render(request, 'admin_panel/enrollments/reject_form.html', context)

@login_required
@user_passes_test(is_staff_member)
def audit_log_view(request):
    """View audit log"""
    query = request.GET.get('q', '')
    
    audit_logs = AuditLog.objects.select_related('user').order_by('-timestamp')
    
    # Apply search filter
    if query:
        audit_logs = audit_logs.filter(
            Q(user__username__icontains=query) |
            Q(action__icontains=query) |
            Q(model_name__icontains=query) |
            Q(description__icontains=query)
        )
    
    context = {
        'audit_logs': audit_logs,
        'query': query,
    }
    return render(request, 'admin_panel/audit_log/list.html', context)

@login_required
@user_passes_test(is_staff_member)
def export_students_csv(request):
    """Export students to CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['رقم الطالب', 'الاسم الأول', 'اسم العائلة', 'البريد الإلكتروني', 'المستوى', 'حالة الاعتماد', 'تاريخ الإنشاء'])
    
    students = Student.objects.all()
    for student in students:
        writer.writerow([
            student.student_id,
            student.first_name,
            student.last_name,
            student.email,
            student.level,
            student.get_approval_status_display(),
            student.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response

@login_required
@user_passes_test(is_staff_member)
def export_courses_csv(request):
    """Export courses to CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="courses.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['كود المقرر', 'اسم المقرر', 'الساعات', 'المعلم المسؤول', 'تاريخ الإنشاء'])
    
    courses = Course.objects.all()
    for course in courses:
        teacher_name = f"{course.teacher.first_name} {course.teacher.last_name}" if course.teacher else "غير محدد"
        writer.writerow([
            course.code,
            course.name,
            course.credit_hours,
            teacher_name,
            course.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response

@login_required
@user_passes_test(is_staff_member)
def export_enrollments_csv(request):
    """Export enrollments to CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="enrollments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['الطالب', 'المقرر', 'الفصل', 'حالة الطلب', 'التقدير', 'تاريخ الطلب', 'تاريخ الاعتماد'])
    
    enrollments = Enrollment.objects.select_related('student', 'course')
    for enrollment in enrollments:
        writer.writerow([
            f"{enrollment.student.first_name} {enrollment.student.last_name}",
            f"{enrollment.course.code} - {enrollment.course.name}",
            enrollment.semester,
            enrollment.get_request_status_display(),
            enrollment.get_grade_display(),
            enrollment.request_date.strftime('%Y-%m-%d %H:%M:%S'),
            enrollment.approval_date.strftime('%Y-%m-%d %H:%M:%S') if enrollment.approval_date else ''
        ])
    
    return response

@login_required
def teacher_dashboard_view(request):
    """Teacher dashboard view - shows courses and students"""
    # Check if user is a teacher
    if not request.user.groups.filter(name='Teachers').exists() and not request.user.is_staff:
        messages.error(request, 'ليس لديك صلاحية الوصول إلى هذه الصفحة.')
        return redirect('student_portal:login')
    
    try:
        teacher = request.user.teacher_profile
        # Get teacher's courses
        courses = Course.objects.filter(teacher=teacher).prefetch_related('enrollments__student')
        
        context = {
            'teacher': teacher,
            'courses': courses,
        }
        return render(request, 'admin_panel/teachers/dashboard.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, 'لم يتم العثور على ملف المعلم الخاص بك.')
        return redirect('student_portal:login')

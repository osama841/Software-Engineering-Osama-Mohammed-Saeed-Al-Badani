from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from students.models import Student, Enrollment, Course
from .forms import StudentForm

@login_required
def complete_profile_view(request):
    """Complete student profile for the first time"""
    student, created = Student.objects.get_or_create(user=request.user, defaults={
        'first_name': request.user.username,
        'student_id': f'STU{request.user.id:06d}',
        'email': request.user.email,
        'approval_status': 'pending'
    })
    
    # If student is already approved, redirect to dashboard
    if student.approval_status == 'approved':
        return redirect('student_portal:dashboard')
    
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
            messages.success(request, 'تم حفظ ملفك الشخصي وتم إرساله للمراجعة.')
            return redirect('student_portal:dashboard')
    else:
        # Pre-populate form with user data
        initial_data = {
            'first_name': request.user.first_name or request.user.username,
            'last_name': student.last_name,
            'student_id': student.student_id,
            'email': student.email,
            'date_of_birth': student.date_of_birth,
            'level': student.level,
        }
        form = StudentForm(initial=initial_data)
    
    return render(request, 'student_portal/complete_profile.html', {'form': form})

@login_required
def edit_profile_view(request):
    """Edit student profile before approval"""
    try:
        student = request.user.student_profile
        # If student is already approved, redirect to dashboard
        if student.approval_status == 'approved':
            messages.error(request, 'لا يمكنك تعديل ملفك بعد اعتماده.')
            return redirect('student_portal:dashboard')
    except Student.DoesNotExist:
        messages.error(request, 'يرجى إكمال ملفك الشخصي أولاً.')
        return redirect('student_portal:complete_profile')
    
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
            messages.success(request, 'تم تحديث ملفك الشخصي.')
            return redirect('student_portal:dashboard')
    else:
        # Pre-populate form with current data
        initial_data = {
            'first_name': student.first_name,
            'last_name': student.last_name,
            'student_id': student.student_id,
            'email': student.email,
            'date_of_birth': student.date_of_birth,
            'level': student.level,
        }
        form = StudentForm(initial=initial_data)
    
    return render(request, 'student_portal/complete_profile.html', {'form': form})

@login_required
def student_dashboard_view(request):
    """Student dashboard view - main page for students"""
    # Check if user is a student
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, 'ليس لديك صلاحية الوصول إلى هذه الصفحة.')
        return redirect('home')
    
    try:
        student = request.user.student_profile
        
        # Check if student profile needs completion
        if student.approval_status == 'pending' and (not student.first_name or not student.last_name):
            messages.info(request, 'يرجى إكمال ملفك الشخصي أولاً.')
            return redirect('student_portal:complete_profile')
        
        # Get student's enrollments
        enrollments = Enrollment.objects.filter(student=student).select_related('course', 'course__teacher')
        
        # Get enrollment statistics
        total_enrollments = enrollments.count()
        approved_enrollments = enrollments.filter(request_status='approved').count()
        pending_enrollments = enrollments.filter(request_status='requested').count()
        
        context = {
            'student': student,
            'enrollments': enrollments,
            'total_enrollments': total_enrollments,
            'approved_enrollments': approved_enrollments,
            'pending_enrollments': pending_enrollments,
        }
        return render(request, 'student_portal/dashboard.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'يرجى إكمال ملفك الشخصي أولاً.')
        return redirect('student_portal:complete_profile')

@login_required
def print_profile_view(request):
    """Print student profile view"""
    try:
        student = request.user.student_profile
        # Get student's enrollments
        enrollments = Enrollment.objects.filter(student=student).select_related('course', 'course__teacher')
        
        context = {
            'student': student,
            'enrollments': enrollments,
        }
        return render(request, 'student_portal/print_profile.html', context)
    except Student.DoesNotExist:
        messages.error(request, 'يرجى إكمال ملفك الشخصي أولاً.')
        return redirect('student_portal:complete_profile')

@login_required
def request_enrollment_view(request):
    """Request enrollment in a course"""
    student = get_object_or_404(Student, user=request.user)
    
    # If student is not approved, they can't request enrollments
    if student.approval_status != 'approved':
        messages.error(request, 'يجب أن يكون ملفك معتمدًا قبل طلب التسجيل في المقررات.')
        return redirect('student_portal:dashboard')
    
    if request.method == 'POST':
        course_id = request.POST.get('course')
        semester = request.POST.get('semester')
        
        if course_id and semester:
            course = get_object_or_404(Course, id=course_id)
            
            # Check if student already requested enrollment in this course for this semester
            existing_enrollment = Enrollment.objects.filter(
                student=student,
                course=course,
                semester=semester
            ).first()
            
            if existing_enrollment:
                messages.error(request, 'لقد قمت بالفعل بطلب التسجيل في هذا المقرر لهذا الفصل.')
            else:
                # Create enrollment request
                Enrollment.objects.create(
                    student=student,
                    course=course,
                    semester=semester,
                    request_status='requested'
                )
                messages.success(request, 'تم إرسال طلب التسجيل بنجاح.')
                return redirect('student_portal:student_enrollments')
        else:
            messages.error(request, 'يرجى اختيار المقرر والفصل.')
    
    # Get available courses
    courses = Course.objects.all()
    # Get current semester (you might want to implement a more sophisticated way to get this)
    current_semester = '2025S1'  # Example semester
    
    context = {
        'courses': courses,
        'current_semester': current_semester,
    }
    return render(request, 'student_portal/request_enrollment.html', context)

@login_required
def student_enrollments_view(request):
    """View student's enrollments"""
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student).select_related('course', 'course__teacher')
    
    context = {
        'student': student,
        'enrollments': enrollments,
    }
    return render(request, 'student_portal/enrollments.html', context)
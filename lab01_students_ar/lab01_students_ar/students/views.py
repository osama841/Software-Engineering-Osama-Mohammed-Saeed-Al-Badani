# students/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import csv

# ============================
# Models
# ============================
from .models import Student, Course, Enrollment, Teacher

# ============================
# Forms
# ============================
from .forms import (
    StudentForm,
    CourseForm,
    EnrollmentForm,
    TeacherForm
)


# ============================
# الصفحة الرئيسية
# ============================
def home(request):
    stats = {
        'students': Student.objects.count(),
        'courses': Course.objects.count(),
        'enrollments': Enrollment.objects.count(),
    }
    top_courses = Course.objects.annotate(num=Count('enrollments')).order_by('-num')[:5]
    return render(request, 'students/home.html', {'stats': stats, 'top_courses': top_courses})


# ===================================================================
#                        Students (الطلاب)
# ===================================================================

# ---------- قائمة الطلاب ----------
@login_required(login_url='/users/login/')
def student_list(request):
    q = request.GET.get('q') or ''
    students = Student.objects.all()
    if q:
        students = students.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)  |
            Q(student_id__icontains=q) |
            Q(email__icontains=q)
        )
    page_obj = Paginator(students.order_by('last_name', 'first_name'), 8).get_page(request.GET.get('page'))
    return render(request, 'students/student_list.html', {'page_obj': page_obj, 'q': q})


# ---------- إنشاء/تعديل ----------
@login_required(login_url='/users/login/')
def student_create(request):
    """
    إنشاء طالب
    """
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Student.objects.create(**form.cleaned_data)
        messages.success(request, "تم إضافة الطالب")
        return redirect("student_list")
    return render(request, "students/form.html", {"form": form, "title": "إضافة طالب"})

@login_required(login_url='/users/login/')
def student_update(request, pk):
    """
    تعديل طالب
    """
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            student.first_name = cd["first_name"]
            student.last_name  = cd["last_name"]
            student.student_id = cd["student_id"]
            student.email      = cd["email"]
            student.date_of_birth = cd.get("date_of_birth")
            student.save()
            messages.success(request, "تم تحديث الطالب")
            return redirect("student_list")
    else:
        form = StudentForm(initial={
            "first_name": student.first_name,
            "last_name":  student.last_name,
            "student_id": student.student_id,
            "email":      student.email,
            "date_of_birth": student.date_of_birth,
        })
    return render(request, "students/form.html", {"form": form, "title": "تعديل طالب"})

@login_required(login_url='/users/login/')
def student_delete(request, pk):
    """
    حذف طالب
    """
    obj = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'تم حذف الطالب')
        return redirect('student_list')
    return render(request, 'students/confirm_delete.html', {'object': obj})


# ---------- تصدير CSV ----------
@login_required(login_url='/users/login/')
def students_export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=students.csv'
    writer = csv.writer(response)
    writer.writerow(['رقم الطالب', 'الاسم الأول', 'اسم العائلة', 'البريد', 'تاريخ الميلاد'])
    for s in Student.objects.all():
        writer.writerow([s.student_id, s.first_name, s.last_name, s.email, s.date_of_birth or ''])
    return response


# ===================================================================
#                        Courses (المقررات)
# ===================================================================

# ---------- قائمة المقررات ----------
@login_required(login_url='/users/login/')
def course_list(request):
    q = request.GET.get('q') or ''
    courses = Course.objects.all()
    if q:
        courses = courses.filter(Q(code__icontains=q) | Q(name__icontains=q))
    page_obj = Paginator(courses.order_by('code'), 10).get_page(request.GET.get('page'))
    return render(request, 'students/course_list.html', {'page_obj': page_obj, 'q': q})
    

# ---------- إنشاء/تعديل ----------
@login_required(login_url='/users/login/')
def course_create(request):
    """
    إنشاء مقرر
    """
    form = CourseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Course.objects.create(**form.cleaned_data)
        messages.success(request, "تم إضافة المقرر")
        return redirect("course_list")
    return render(request, "students/form.html", {"form": form, "title": "إضافة مقرر"})

@login_required(login_url='/users/login/')
def course_update(request, pk):
    """
    تعديل مقرر
    """
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            course.code         = cd["code"]
            course.name         = cd["name"]
            course.credit_hours = cd["credit_hours"]
            course.save()
            messages.success(request, "تم تحديث المقرر")
            return redirect("course_list")
    else:
        form = CourseForm(initial={
            "code": course.code,
            "name": course.name,
            "credit_hours": course.credit_hours,
        })
    return render(request, "students/form.html", {"form": form, "title": "تعديل مقرر"})

@login_required(login_url='/users/login/')
def course_delete(request, pk):
    """
    حذف مقرر
    """
    obj = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'تم حذف المقرر')
        return redirect('course_list')
    return render(request, 'students/confirm_delete.html', {'object': obj})


# ===================================================================
#                      Enrollments (التسجيلات)
# ===================================================================

# ---------- قائمة التسجيلات ----------
@login_required(login_url='/users/login/')
def enrollment_list(request):
    q = request.GET.get('q') or ''
    semester = request.GET.get('semester') or ''
    enrollments = Enrollment.objects.select_related('student', 'course').all()
    if q:
        enrollments = enrollments.filter(
            Q(student__student_id__icontains=q) |
            Q(student__first_name__icontains=q) |
            Q(student__last_name__icontains=q)  |
            Q(course__code__icontains=q)        |
            Q(course__name__icontains=q)
        )
    if semester:
        enrollments = enrollments.filter(semester__icontains=semester)
    page_obj = Paginator(enrollments.order_by('-id'), 12).get_page(request.GET.get('page'))
    return render(request, 'students/enrollment_list.html', {'page_obj': page_obj, 'q': q, 'semester': semester})


# ---------- إنشاء/تعديل ----------
@login_required(login_url='/users/login/')
def enrollment_create(request):
    """
    إنشاء تسجيل
    """
    form = EnrollmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Enrollment.objects.create(
            student=form.cleaned_data["student"],
            course=form.cleaned_data["course"],
            semester=form.cleaned_data["semester"],
            grade=form.cleaned_data.get("grade") or None,
        )
        messages.success(request, "تم إضافة التسجيل")
        return redirect("enrollment_list")
    return render(request, "students/form.html", {"form": form, "title": "إضافة تسجيل"})

@login_required(login_url='/users/login/')
def enrollment_update(request, pk):
    """
    تعديل تسجيل
    """
    enr = get_object_or_404(Enrollment, pk=pk)
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enr.student  = form.cleaned_data["student"]
            enr.course   = form.cleaned_data["course"]
            enr.semester = form.cleaned_data["semester"]
            enr.grade    = form.cleaned_data.get("grade") or None
            enr.save()
            messages.success(request, "تم تحديث التسجيل")
            return redirect("enrollment_list")
    else:
        form = EnrollmentForm(initial={
            "student":  enr.student,
            "course":   enr.course,
            "semester": enr.semester,
            "grade":    enr.grade,
        })
    return render(request, "students/form.html", {"form": form, "title": "تعديل تسجيل"})

@login_required(login_url='/users/login/')
def enrollment_delete(request, pk):
    """
    حذف تسجيل
    """
    obj = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'تم حذف التسجيل')
        return redirect('enrollment_list')
    return render(request, 'students/confirm_delete.html', {'object': obj})


# ===================================================================
#                         Teachers (المعلّمون)
# ===================================================================

# ---------- قائمة المعلّمين ----------
@login_required(login_url='/users/login/')
def teacher_list(request):
    q = request.GET.get("q", "")
    qs = Teacher.objects.all()
    if q:
        qs = qs.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)  |
            Q(email__icontains=q)      |
            Q(department__icontains=q)
        )
    page_obj = Paginator(qs.order_by("last_name", "first_name"), 10).get_page(request.GET.get("page"))
    return render(request, "students/teachers/list.html", {"page_obj": page_obj, "q": q})


# ---------- إنشاء/تعديل ----------
@login_required(login_url='/users/login/')
def teacher_create(request):
    """
    إنشاء معلّم
    """
    form = TeacherForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            Teacher.objects.create(**form.cleaned_data)
        except IntegrityError:
            form.add_error("email", "هذا البريد مستخدم من قبل.")
        else:
            messages.success(request, "تم إضافة المعلّم")
            return redirect("teacher_list")
    return render(request, "students/teachers/from.html", {"form": form, "title": "إضافة معلّم"})

@login_required(login_url='/users/login/')
def teacher_update(request, pk):
    """
    تعديل معلّم
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            teacher.first_name = cd["first_name"]
            teacher.last_name  = cd["last_name"]
            teacher.email      = cd["email"]
            teacher.phone      = cd.get("phone")
            teacher.department = cd.get("department")
            try:
                teacher.save()
            except IntegrityError:
                form.add_error("email", "هذا البريد مستخدم من قبل.")
            else:
                messages.success(request, "تم تحديث بيانات المعلّم")
                return redirect("teacher_list")
    else:
        form = TeacherForm(initial={
            "first_name": teacher.first_name,
            "last_name":  teacher.last_name,
            "email":      teacher.email,
            "phone":      teacher.phone,
            "department": teacher.department,
        })
    return render(request, "students/teachers/from.html", {"form": form, "title": "تعديل معلّم"})

@login_required(login_url='/users/login/')
def teacher_delete(request, pk):
    """
    حذف معلّم
    """
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        teacher.delete()
        messages.success(request, "تم حذف المعلم")
        return redirect("teacher_list")
    return render(request, "students/confirm_delete.html", {"object": teacher})
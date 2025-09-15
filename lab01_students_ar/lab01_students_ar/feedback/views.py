from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.utils import timezone
from django.contrib import messages
from .forms import FeedbackForm

def submit_feedback(request):
    """Submit feedback form"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Process the form data
            student_name = form.cleaned_data['student_name']
            email = form.cleaned_data['email']
            course_name = form.cleaned_data['course_name']
            understanding_level = form.cleaned_data['understanding_level']
            positives = form.cleaned_data['positives']
            negatives = form.cleaned_data['negatives']
            improvements = form.cleaned_data['improvements']
            comparison = form.cleaned_data['comparison']
            future_use = form.cleaned_data['future_use']
            
            # Prepare email content
            context = {
                'student_name': student_name,
                'email': email,
                'course_name': course_name,
                'understanding_level': understanding_level,
                'positives': positives,
                'negatives': negatives,
                'improvements': improvements,
                'comparison': comparison,
                'future_use': future_use,
                'today': timezone.now()
            }
            
            html_body = render_to_string("feedback/feedback_email.html", context)
            
            subject = f"انطباع الطالب: {student_name} - {course_name}"
            from_email = email  # Student's email
            to_emails = ["osamma.b7@gmail.com"]  # Teacher's email
            
            connection = get_connection(
                backend="django.core.mail.backends.smtp.EmailBackend",
                host="smtp.gmail.com",
                port=587,
                username="YOUR_GMAIL@gmail.com",
                password="YOUR_APP_PASSWORD",  # App Password from Google
                use_tls=True,
            )
            
            msg = EmailMessage(
                subject=subject,
                body=html_body,
                from_email=from_email,
                to=to_emails,
                connection=connection,
            )
            msg.content_subtype = "html"  # Send as HTML
            sent = msg.send()
            
            if sent:
                return render(request, 'feedback/success.html')
            else:
                messages.error(request, '❌ فشل إرسال الانطباع. يرجى المحاولة مرة أخرى.')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء في النموذج.')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/submit.html', {'form': form})

def send_feedback_email(request):
    """Legacy feedback email function"""
    # جهّز الـ HTML من القالب (بدون أي متغيرات إضافية)
    html_body = render_to_string("feedback/feedback_email.html", {"today": timezone.now()})

    subject = "انطباع الطالب: أسامة محمد سعيد سلام البعداني"
    from_email = "aalbdany054@gmail.com"        # بريدك
    to_emails  = ["osamma.b7@gmail.com"]   # بريد الدكتور

    connection = get_connection(
        backend="django.core.mail.backends.smtp.EmailBackend",
        host="smtp.gmail.com",
        port=587,
        username="YOUR_GMAIL@gmail.com",
        password="YOUR_APP_PASSWORD",  # App Password من جوجل
        use_tls=True,
    )

    msg = EmailMessage(
        subject=subject,
        body=html_body,
        from_email=from_email,
        to=to_emails,
        connection=connection,
    )
    msg.content_subtype = "html"  # عشان يرسل كـ HTML
    sent = msg.send()

    return HttpResponse("✅ تم إرسال الرسالة بنجاح" if sent else "❌ فشل الإرسال")
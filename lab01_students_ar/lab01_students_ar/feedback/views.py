from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, get_connection
from django.utils import timezone

def send_feedback_email(request):
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

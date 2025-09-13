from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives

AR_MONTHS = ["يناير","فبراير","مارس","أبريل","مايو","يونيو",
             "يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]

STUDENT_NAME = "أسامة محمد سعيد سلام البعداني"

def auto_send(request):
    now = timezone.localtime()
    today_str = f"{now.day:02d} {AR_MONTHS[now.month-1]} {now.year}"

    ctx = {"student_name": STUDENT_NAME, "today_str": today_str}
    html_body = render_to_string("mailer/email.html", ctx)
    text_body = strip_tags(html_body)

    subject = STUDENT_NAME
    connection = get_connection()

    # المرسِل والمُستقبل = نفس البريد
    sender = settings.EMAIL_HOST_USER
    recipients = [settings.EMAIL_HOST_USER]  # أو settings.TEACHER_EMAIL (نفسه هنا)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=sender,      # ← نفس بريدك بالضبط
        to=recipients,          # ← نفس بريدك
        connection=connection,
        reply_to=[sender],
    )
    msg.attach_alternative(html_body, "text/html")

    try:
        sent = msg.send()
        return HttpResponse(f"✅ تم الإرسال | From={sender} | To={recipients} | sent={sent}")
    except Exception as e:
        return HttpResponse(f"❌ فشل الإرسال: {type(e).__name__}: {e}", status=500)

# (اختياري) فحص القيم
def diag(request):
    return JsonResponse({
        "EMAIL_BACKEND": settings.EMAIL_BACKEND,
        "EMAIL_HOST_USER": settings.EMAIL_HOST_USER,
        "DEFAULT_FROM_EMAIL": settings.DEFAULT_FROM_EMAIL,
        "TEACHER_EMAIL": settings.TEACHER_EMAIL,
    })
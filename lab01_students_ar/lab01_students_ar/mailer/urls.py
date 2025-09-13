from django.urls import path
from django.http import HttpResponse
from .views import auto_send

app_name = "mailer"

def index(request):
    return HttpResponse("مرحبًا بك في تطبيق المراسلة (Mailer)!")

urlpatterns = [
    path("", index, name="index"),             # /mailer/
    path("auto-send/", auto_send, name="auto_send"),
]

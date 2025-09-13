from django.urls import path
from .views import send_feedback_email

urlpatterns = [
    path("send/", send_feedback_email, name="feedback_send"),
]

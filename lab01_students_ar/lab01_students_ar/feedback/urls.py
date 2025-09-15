from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path("send/", views.send_feedback_email, name="feedback_send"),
    path("submit/", views.submit_feedback, name="submit_feedback"),
]
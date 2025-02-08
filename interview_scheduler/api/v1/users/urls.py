from django.urls import re_path
from . import views

app_name = "api_v1_users"

urlpatterns = [
    re_path(r'^signup/', views.signup, name='signup'),
    re_path(r'^signin/', views.signin, name='signin'),

    re_path(r'^add-interview-availability/', views.add_interview_availability, name='add_interview_availability'),
    re_path(r'^get-possible-interviews/', views.get_possible_interviews, name='get_possible_interviews'),
]
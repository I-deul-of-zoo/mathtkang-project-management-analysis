from django.urls import path
from teams import views

app_name = "teams"

urlpatterns =[
    path("", views.TeamCreation.as_view()),
    path("<int:id>/invi", views.TeamInvitation.as_view()),
    path("<int:id>/accept", views.TeamInvitationAcceptance.as_view()),
]
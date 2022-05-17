from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("NewSession", views.Sessions, name="Sessions"),
    path("timedurr", views.TimeDuration, name="timeduration"),
    path("delstu/<int:id>/", views.deleteStudent, name="deleteStudent"),
    path("signOut/<int:id>/", views.signOut, name="signOut"),
    path("allStudents", views.allStudents,name="allStudents"),
    path("addHours/<int:id>",views.addHours,name="AddHours")
]

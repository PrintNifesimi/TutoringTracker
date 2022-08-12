from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginPage, name="loginPage"),
    path("login/",views.loginPage, name="loginPage"),
    path("logout/", views.logoutUser, name="logout"),
    path("NewSession", views.Sessions, name="Sessions"),
    path("timedurr", views.TimeDuration, name="timeduration"),
    path("delstu/<int:id>/", views.deleteStudent, name="deleteStudent"),
    path("signOut/<int:id>/", views.signOut, name="signOut"),
    path("allStudents", views.allStudents,name="allStudents"),
    path("addHours/<int:id>",views.addHours,name="AddHours"),
    path("Export",views.studentExport_txt,name="studentExport_txt"),
    path("Export_csv",views.studentExport_csv,name='studentExport_csv')
]

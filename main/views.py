import datetime
import imp
import math
from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpRequest
from .models import Students,Session
from pytz import timezone
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from django.views.decorators.csrf import csrf_protect

#from .forms import sessionForm

# Create your views here.

def index(response):
    studentsList = Students.objects.all().order_by('firstName')
    context={"Students":studentsList}
    return render(response, "main/AllStudents.html", context)

@require_http_methods(['GET','POST'])
@csrf_protect
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('allStudents')
    else:
        invalidUser = False
        if request.method == 'POST':
            username =request.POST.get("userName")
            password=request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('allStudents')  
            else:
                invalidUser = True
        context={"invalidUser":invalidUser}
        return render(request, "main/loginPage.html",context)

@require_http_methods(['GET','POST'])
def logoutUser(request):
    logout(request)
    return redirect('loginPage')




@require_http_methods(['GET','POST'])
@login_required(login_url='loginPage')
def Sessions(response):
    
    sesh=Session.objects.all().order_by('fullname')
    stud=Students.objects.all().order_by('firstName')
    
    badAddAlert=False
    nullAddAlert=False
    endSessionAlert=False
    if response.method == "POST":
        
        if response.POST.get("addStudent") or response.POST.get("addStudent")=="":
            newStudentSession=Session(currDuration=datetime.timedelta(hours=0))
            newStudentSession.fullname=response.POST.get("addStudent")
            if newStudentSession.fullname=="" or newStudentSession.fullname.isspace():
                    nullAddAlert=True
            if newStudentSession.fullname not in str(stud):
                nullAddAlert=True
            for studentsession in sesh:
                if studentsession.fullname == newStudentSession.fullname:
                    badAddAlert=True
                    break
            if badAddAlert!=True and nullAddAlert!=True:
                    newStudentSession.save()
            context={"sObject":sesh,"Stud":stud,"badAddAlert":badAddAlert,"nullAddAlert":nullAddAlert,"endSessionAlert":endSessionAlert}
            return render(response,"main/partials/Timeduration.html",context)      
            
        if response.POST.get("endSession"):
            eastern=timezone('US/Eastern')
            time_now=datetime.datetime.now(eastern)
            nwlst=[]
            for sess in sesh:
                nwlst.append(str(sess.fullname))
            for item in stud:
                    if item.toString() in nwlst:
                        calculatedT=time_now-Session.objects.get(fullname=item.toString()).currDuration
                        toSeconds=calculatedT.seconds+item.totalSeconds()
                        newHours= toSeconds/3600
                        item.hours=int(newHours)
                        item.minutes=(newHours*60)%60
                        item.save()
            endSessionAlert=True
            sesh.delete()
    context={"sObject":sesh,"Stud":stud,"badAddAlert":badAddAlert,"nullAddAlert":nullAddAlert,"endSessionAlert":endSessionAlert}
    return render(response, "main/sessions.html", context)

def TimeDuration(request):
    sesh=Session.objects.all().order_by('fullname')
    stud=Students.objects.all()
    badAddAlert=False
    nullAddAlert=False
    endSessionAlert=False
    signOutSuccess=False
    context={"sObject":sesh,"Stud":stud,"badAddAlert":badAddAlert,"nullAddAlert":nullAddAlert,"endSessionAlert":endSessionAlert,"signOutSuccess":signOutSuccess}
    return render(request,"main/partials/Timeduration.html",context)

@require_http_methods(['DELETE'])
def deleteStudent(response, id):
    Session.objects.get(id=id).delete()
    sesh=Session.objects.all().order_by('fullname')
    stud=Students.objects.all()
    badAddAlert=False
    nullAddAlert=False
    endSessionAlert=False
   
    context={"sObject":sesh,"Stud":stud,"badAddAlert":badAddAlert,"nullAddAlert":nullAddAlert,"endSessionAlert":endSessionAlert}

    return render(response, "main/partials/Timeduration.html",context)

@require_http_methods(['POST'])
def signOut(response, id):
    student = Session.objects.get(id=id)
    sesh=Session.objects.all().order_by('fullname')
    stud=Students.objects.all().order_by('firstName')
    badAddAlert=False
    nullAddAlert=False
    endSessionAlert=False
    signOutSuccess=False
    
    eastern=timezone('US/Eastern')
    time_now=datetime.datetime.now(eastern)
    
    calculatedT=time_now-student.currDuration
    
    for item in stud:
        if student.fullname == item.toString():
            
            toSeconds=calculatedT.seconds+item.totalSeconds()
            newHours= toSeconds/3600
            item.hours=int(newHours)
            item.minutes=(newHours*60)%60
            item.save()
            student.delete()
            signOutSuccess=True
            break





    context={"sObject":sesh,"Stud":stud,"badAddAlert":badAddAlert,"nullAddAlert":nullAddAlert,"endSessionAlert":endSessionAlert,"signOutSuccess":signOutSuccess}

    return render(response, "main/partials/Timeduration.html",context)

@login_required(login_url='loginPage')
@csrf_protect
def allStudents(response):
    studentsList = Students.objects.all().order_by('firstName')
    context={"Students":studentsList}
    return render(response,"main/AllStudents.html",context)

@require_http_methods(['POST','GET'])
def addHours(response,id):
    
    studentsList = Students.objects.all().order_by('firstName')
    studentID = id
    nullHourAdd = False
    editStudent = False
    successAdd = False
    student = Students.objects.get(id=id)
    
    if response.method == 'GET' and not editStudent:
        editStudent = True
        
        context={"Students":studentsList,"editStudent":editStudent,"studentID":studentID,"nullHourAdd":nullHourAdd,"successAdd":successAdd}
        return render(response,"main/partials/AddHours.html",context)
        
    if response.method == 'POST': 
        if response.POST.get("AddedHours")!="" and not response.POST.get("AddedHours").isspace() and response.POST.get("AddedMinutes")!="" and not response.POST.get("AddedMinutes").isspace():
            addedTime = (float(response.POST.get("AddedHours"))*3600)+(float(response.POST.get("AddedMinutes"))*60)+student.totalSeconds()
            
            student.hours = int(addedTime/3600)
            student.minutes = ((addedTime/3600)*60)%60
            successAdd = True
            student.save()
            
            context={"Students":studentsList,"editStudent":editStudent,"studentID":studentID,"nullHourAdd":nullHourAdd,"successAdd":successAdd}
            return render(response,"main/partials/AddHours.html",context)
        elif response.POST.get("AddedHours").isspace() or response.POST.get("AddedHours")=="" or response.POST.get("AddedMinutes").isspace() or response.POST.get("AddedMinutes")=="":
            editStudent = True
            nullHourAdd = True
           
            context={"Students":studentsList,"editStudent":editStudent,"studentID":studentID,"nullHourAdd":nullHourAdd,"successAdd":successAdd}
            return render(response,"main/partials/AddHours.html",context)
    
    
def studentExport_txt(request):
    response=HttpResponse(content_type='text/plain')   
    response['Content-Disposition'] = 'attachment; filename=Export_txt.txt'
    students = Students.objects.all().order_by('firstName')
    lines = []
    for student in students:
        strVar = str(student) + ' ---> '+str(student.hours)+' hours, '+str(student.minutes)+' minutes'+'\n'
        lines.append(strVar)

    

    response.writelines(lines)
    return response

def studentExport_csv(request):
    response=HttpResponse(content_type='text/csv')   
    response['Content-Disposition'] = 'attachment; filename=Export_csv.csv'
    writer = csv.writer(response)
    students = Students.objects.all().order_by('firstName')
    writer.writerow(['Student Name','Time'])

    for student in students:
        strVar =str(student.hours)+' hours, '+str(student.minutes)+' minutes'
        writer.writerow([student,strVar])

    

    
    return response

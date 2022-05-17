import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpRequest
from .models import Students,Session
from pytz import timezone
from django.views.decorators.http import require_http_methods

#from .forms import sessionForm

# Create your views here.

def index(response):
    studentsList = Students.objects.all()
    context={"Students":studentsList}
    return render(response, "main/AllStudents.html", context)

@require_http_methods(['GET','POST'])
def Sessions(response):
    sesh=Session.objects.all().order_by('fullname')
    stud=Students.objects.all()
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
    stud=Students.objects.all()
    badAddAlert=False
    nullAddAlert=False
    endSessionAlert=False
    signOutSuccess=False
    
    eastern=timezone('US/Eastern')
    time_now=datetime.datetime.now(eastern)
    
    calculatedT=time_now-student.currDuration
    
    for item in stud:
        if str(student.fullname) == item.toString():
            toSeconds=calculatedT.seconds+item.totalSeconds()
            newHours= toSeconds/3600
            item.hours=int(newHours)
            item.minutes=(newHours*60)%60
            item.save()
            student.delete()
            signOutSuccess=True





    context={"sObject":sesh,"Stud":stud,"badAddAlert":badAddAlert,"nullAddAlert":nullAddAlert,"endSessionAlert":endSessionAlert,"signOutSuccess":signOutSuccess}

    return render(response, "main/partials/Timeduration.html",context)

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
    
    
    

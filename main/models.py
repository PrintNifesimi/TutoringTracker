from django.db import models
import datetime
from datetime import time, timezone

# Create your models here.
class Students(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    hours=models.IntegerField(default=0)
    minutes=models.IntegerField(default=0)
    
    def getFirstName(self):
        return self.firstName
    def getLastName(self):
        return self.lastName
    def totalSeconds(self):
        return (self.hours*3600)+(self.minutes*60)
    #def time(self):
        #return ((self.hours*3600)+(self.minutes*60))/3600
    def __str__(self) -> str:
        return self.firstName + " "+self.lastName
    def toString(self) -> str:
        return self.firstName+" "+self.lastName 
    
        

class Session(models.Model):
    currDuration = models.DateTimeField(auto_now_add=True)
    stud=Students()
    fullname = models.CharField(max_length=100,null=True)

    def __str__(self) -> str:
        return self.fullname + " " + str(self.currDuration)


    
    


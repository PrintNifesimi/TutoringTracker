from django.contrib import admin
from .models import Session, Students
from django.urls import path
from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# Register your models here.

class studentImportForm(forms.Form):
    csv_upload = forms.FileField()



class StudentsAdmin(admin.ModelAdmin):
    
    def get_urls(self):
        urls= super().get_urls()
        new_urls = [path("upload-csv/", self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(('.txt','.csv')):
                
                messages.warning(request, 'You are trying to upload the wrong file, make sure it is a csv or text file')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            
            for x in csv_data:
                if not x.isspace() and x != "":
                    fields = x.split(" ")
                    created = Students.objects.create(
                        firstName = fields[0].replace('\r', ''),
                        lastName = fields[1].replace('\r', ''),
                    )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)
        form = studentImportForm()
        data = {"form":form}
        return render(request, "admin/studentImport.html",data)

admin.site.register(Students,StudentsAdmin)
admin.site.register(Session)

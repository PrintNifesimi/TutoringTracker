from django import forms

class sessionForm(forms.Form):
    Fullname=forms.CharField(label="Full Name", max_length=100)
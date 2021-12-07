from django import forms
from django.contrib.auth.models import User
from . import models
from .models import khaas



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']

        
#pharmacoligst related form 
class laboratoristUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class laboratoristForm(forms.ModelForm):
    
    class Meta:
        model=models.laboratorist
        fields=['address','mobile','test','status','profile_pic']



#for patient related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):

    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="choose doctor ,if no option then there must be doctor", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','profile_pic',"age"]

class treatmentForm(forms.ModelForm):
    assignedDoctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),
                                      empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.treatment
        fields="__all__"



class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
#for notice related form
  
class massagesForm(forms.ModelForm):
    # to=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name ", to_field_name="user_id")
    class Meta:
        model=models.massages
        fields='__all__'
    
    



class treatmentForm(forms.ModelForm):
    class Meta:
        model=models.treatment
        fields="__all__"






class khaasform(forms.ModelForm):
    class Meta:
        model = models.khaas
        fields = "__all__"


    def __init__(self ,*args,**kwargs):
        super(khaasform, self).__init__(*args,**kwargs)
        self.fields['to'].empty_label="select user"






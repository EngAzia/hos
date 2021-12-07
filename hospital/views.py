from django.shortcuts import render,redirect,reverse
from django.db.models import Sum
from django.contrib.auth.models import Group,User
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.contrib import messages
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse
from .filters import *
from . import models,forms

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    show=models.instructions.objects.all()
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html' ,{"show":show})
#for showing sigup/login button for labarotosirt 
def laboratoristclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/laboratoristclick.html')


def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            global test;
            test=user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            if test:
                messages.error(request,("failed to register"));
            else:
                messages.success(request,("registeration done successfully"));
    return render(request,'hospital/adminsignup.html',{'form':form});




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user # this creates the actual link between doctor and uer
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def laboratorist_signup_view(request):
    userForm=forms.laboratoristUserForm()
    laboratorisform=forms.laboratoristForm()
    mydict={'userForm':userForm,'Form':laboratorisform}
    if request.method=='POST':
        userForm=forms.laboratoristUserForm(request.POST)
        laboratoristForm=forms.laboratoristForm(request.POST,request.FILES)
        if userForm.is_valid() and laboratoristForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            laboratorist= laboratoristForm.save(commit=False)
            laboratorist.user=user
            laboratorist= laboratorist.save()
            my_doctor_group = Group.objects.get_or_create(name='laboratorist')
            my_doctor_group[0].user_set.add(user)
            return HttpResponseRedirect('laboratoristlogin')
    return render(request,'hospital/laboratoristsignup.html',context=mydict)
        
    


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/patientsignup.html',context=mydict)








#-----------for checking user is doctor , patient or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_laboratorist(user):
    return user.groups.filter(name='laboratorist').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT and labaratorist
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')
    elif is_laboratorist(request.user):
        accountapproval=models.laboratorist.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('laboratorist-dashboard')
        else:
            return render(request,'hospital/laboratorist_wait_for_approval.html')
  








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    laboratorist=models.laboratorist.objects.all().order_by('-id')
    #for five user cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()
    laboratoristcount=models.laboratorist.objects.all().filter(status=True).count()
    laboratoristpendingcount=models.laboratorist.objects.all().filter(status=False).count()
    TestRequestcount=models.shaybaadh.objects.all().count()
    Testpendingcount=models.shaybaadh.objects.all().count()
    massages=models.massages.objects.all()
    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    #cities report
    ceerigabo = models.Patient.objects.all().filter(address="ceerigabo").count()
    city = models.Patient.objects.all().filter(address="hargeisa").count()
    gabilay = models.Patient.objects.all().filter(address="gabilay").count()
    borama = models.Patient.objects.all().filter(address="borama").count()
    burco = models.Patient.objects.all().filter(address="burco").count()
    saylac = models.Patient.objects.all().filter(address="saylac").count()
    odwayne = models.Patient.objects.all().filter(address="odwayne").count()
    caynabo = models.Patient.objects.all().filter(address="caynabo").count()

    barbara = models.Patient.objects.all().filter(address="barbara").count()

    khaas=models.khaas.objects.all().filter(to=request.user)

    #diagnosis report


    allergic=models.treatment.objects.all().filter(diagnosis="allergic").count()

    flu = models.treatment.objects.all().filter(diagnosis="flu").count()
    glucoma=models.treatment.objects.all().filter(diagnosis="glucoma").count()
    tp = models.treatment.objects.all().filter(diagnosis="tp").count()
    retinitis = models.treatment.objects.all().filter(diagnosis="retinitis").count()
    hiv = models.treatment.objects.all().filter(diagnosis="hiv").count()
    malaria = models.treatment.objects.all().filter(diagnosis="malaria").count()


    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    
    'laboratoristcount':laboratoristcount,
    'laboratoristpendingcount':laboratoristpendingcount,
    'TestRequestcount':TestRequestcount,
    'Testpendingcount':Testpendingcount,
    'massages':massages,
    'khaas':khaas,
    'city':city,
    'ceerigabo':ceerigabo,
    'gabilay':gabilay,
    'borama':borama,
    'burco':burco,
    'barbara':barbara,
    'malaria':malaria,
    'hiv':hiv,
    'allergic':allergic,
    'malaria': malaria,
    'tp': tp,
    'glucoma': glucoma,
    'flu': flu,





    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def fariimaha(request):

    massages = models.massages.objects.all()
    khaas = models.khaas.objects.all().filter(to=request.user)
    mydict={
        'massages':massages,
        'khaas':khaas,


    }
    return render(request, 'hospital/fariimaha.html', context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_report_view(request):
    return render(request, 'hospital/admin_report.html', {})

# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_laboratorist_view(request):
    return render(request,'hospital/admin_laboratorist.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def patient_state_veiw(request):

    return render(request,"patient_state.html")


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form = forms.massagesForm()
    if request.method == 'POST':
        form = forms.massagesForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.by = request.user.first_name + " " + request.user.last_name

            form.save()
            return redirect('admin-dashboard')
    return render(request, 'hospital/admin_notice.html', {'form': form})


def admin_khaas_view(request):
 form=forms.khaasform()
 if request.method == 'POST':
     form=forms.khaasform(request.POST)
     if form.is_valid():
         form = form.save(commit=False)
         form.by = request.user.first_name + " " + request.user.last_name

         form=form.save()
         return redirect('admin-dashboard')

 return render(request,'hospital/admin_khaas.html', {'form': form})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctorfilter= DoctorFilter(request.GET, queryset=models.Doctor.objects.all().filter(status=True)),

    mydic={
        'doctorfilter' : DoctorFilter(request.GET, queryset=models.Doctor.objects.all().filter(status=True)),
        'doctors' : models.Doctor.objects.all().filter(status=True),

    }


    return render(request,'hospital/admin_view_doctor.html', context=mydic)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_laboratorist_view(request):
    laboratorist=models.laboratorist.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_laboratorist.html',{'laboratorist':laboratorist})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_laboratorist_view(request,pk):
    laboratorist=models.laboratorist.objects.get(id=pk)
    user=models.User.objects.get(id=laboratorist.user_id)

    userForm=forms.laboratoristUserForm(instance=user)
    laboratoristForm=forms.laboratoristForm(request.FILES,instance=laboratorist)
    mydict={'userForm':userForm,'laboratoristForm':laboratoristForm}
    if request.method=='POST':
        userForm=forms.laboratoristUserForm(request.POST,instance=user)
        laboratoristForm=forms.laboratoristForm(request.POST,request.FILES,instance=laboratorist)
        if userForm.is_valid() and laboratoristForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            laboratorist=laboratoristForm.save(commit=False)
            laboratorist.status=True
           # laboratorist.assignedDoctorId=request.POST.get('assignedDoctorId')
            laboratorist.save()
            return redirect('admin-view-laboratorist')
    return render(request,'hospital/admin_update_laboratorist.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()
            

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)

#ading labaratorist by admin 
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_laboratorist_view(request):
    userForm=forms.laboratoristUserForm()
    laboratorisform=forms.laboratoristForm()
    mydict={'userForm':userForm,'laboratoristForm':laboratorisform}
    if request.method=='POST':
        userForm=forms.laboratoristUserForm(request.POST)
        laboratoristForm=forms.laboratoristForm(request.POST,request.FILES)
        if userForm.is_valid() and laboratoristForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            laboratorist= laboratoristForm.save(commit=False)
            laboratorist.user=user
            laboratorist.status=True
            laboratorist= laboratorist.save()
            my_doctor_group = Group.objects.get_or_create(name='laboratorist')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-laboratorist')
    return render(request,'hospital/admin_add_laboratorist.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def report(request):
  
  return render(request,"hospital/admin_report.html");
#end of adding labaratorist by admin 



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_laboratorist_view(request):
    #those whose approval are needed
    laboratorist=models.laboratorist.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_laboratorist.html',{'laboratorist':laboratorist})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_laboratorist_view(request,pk):
    laboratorist=models.laboratorist.objects.get(id=pk)
    laboratorist.status=True
    laboratorist.save()
    return redirect(reverse('admin-approve-laboratorist'))




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_laboratorist_view(request,pk):
    laboratorist=models.laboratorist.objects.get(id=pk)
    user=models.User.objects.get(id=laboratorist.user_id)
    user.delete()
    laboratorist.delete()
    return redirect('admin-approve-laboratorist')


    



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')







@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)









@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.treatment.objects.filter(patientid__status=True)



    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    treatment=models.treatment.objects.get(id=pk)
    days=(date.today()-treatment.patientid.admitDate) #example 6 days
    assignedDoctor=models.User.objects.all().filter(id=treatment.patientid.assignedDoctorId)
    d=days.days # only how many day for example is 2

    patientDict={
        'patientId':pk,
        'name':treatment.patientid.get_name,
        'mobile':treatment.patientid.mobile,
        'address':treatment.patientid.address,
        'symptoms':treatment.symptoms,
        'diagnosis': treatment.diagnosis,
        'treatment':treatment.treatment,
        'medicne':treatment.medicne,
        'admitDate':treatment.patientid.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()

        pDD.patientId=pk
        pDD.patientName=treatment.patientid.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=treatment.patientid.address
        pDD.mobile=treatment.patientid.mobile
        pDD.symptoms=treatment.symptoms
        pDD.diagnosis = treatment.diagnosis
        pDD.treatment=treatment.treatment
        pDD.treatment=treatment.medicne
        pDD.admitDate=treatment.patientid.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge']))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'diagnosis': dischargeDetails[0].diagnosis,
        'treatment':dischargeDetails[0].treatment,
        'medicne':dischargeDetails[0].medicne,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')



#-----------------test START--------------------------------------------------------------------



#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------------ Labarotorist RELATED VIEWS START ------------------------------
#-----------------------------------------_----------------------------------------



#---------------------------------------------------------------------------------
#------------------------ labaratorist  RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
# @login_required(login_url='laboratoristlogin')
# @user_passes_test(is_laboratorist)

# def laboratorist_dashboard_view(request):
    



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards

    massages = models.massages.objects.all()
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')

    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    khaas = models.khaas.objects.all().filter(to=request.user)


    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'khaas':khaas,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id),
     #for profile picture of doctor in sidebar
     'massages':massages,

    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_treatment_view(request):
    form=forms.treatmentForm()
    mydic={"form":form}
    if request.POST:
        form=forms.treatmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("doctor-dashboard")
    return  render(request,"hospital/doctor_treatment.html",context=mydic)




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_notice_view(request):
    current_user = request.user
    user = current_user.id
    form = forms.tomassagesForm()
    massages = models.tomassages.objects.all().filter(m_participant=request.user)
    if request.method == 'POST':
        form = forms.tomassagesForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.byo = request.user.first_name + "  " + request.user.last_name

            form.save()
            return redirect('doctor-dashboard')
    return render(request, 'hospital/doctor_notice.html', {'form': form})


#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    khaas = models.khaas.objects.all().filter(to=request.user.id)
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    massages = models.massages.objects.all()
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'profile':doctor.profile_pic,

    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    'massages': massages,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():

            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)





@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------

def doctor_khaas_view(request):
 form=forms.khaasform()
 if request.method == 'POST':
     form=forms.khaasform(request.POST)
     if form.is_valid():
         form = form.save(commit=False)
         form.by = request.user.first_name + " " + request.user.last_name

         form=form.save()
         return redirect('doctor-dashboard')

 return render(request,'hospital/doctor_khaas.html', {'form': form})






#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


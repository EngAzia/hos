from django.db import models
from django.contrib.auth.models import User


departments=[
('dhaqtarka indhaha','optometrist'),
('cardiologist','dhaqtarka wadnaha'),
('Dermatologists','dhaqtarka maqaarka'),
('Emergency Medicine Specialists','dhaqtarka xaalad dagdag ah'),
('Allergists/Immunologists','dhaqtarka alarjiga'),
('Anesthesiologists','dhaqtarka suuxdinta'),

]

Addres=[
('hargeisa','hargeisa'),
('borama','borama'),
('gabilay','gabilay'),
('burco','burco'),
('ceerigabo','ceerigabo'),
('odwayne','odwayne'),
('saylac','saylac'),
('caynabo','caynabo'),
('laascanod','laascanod'),
('arabsiyo','arabsiyo'),
('oodwayne','oodwayne'),
('barbara','barbara'),

('magaalo kale','magaalo kale'),

]


op=[
('inpatient','inpatient'),
("outpatient","oupatient"),

]

testo=[('blood','blood'),
('urine','urine'),
]



class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address= models.CharField(max_length=50,choices=Addres,default='hargeisa')
    mobile = models.CharField(max_length=20,unique=True)
    department= models.CharField(max_length=50,choices=departments,default='optometrist')
    status=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

    class Meta:
        db_table = "doctor"


#return "{} ({}).format" this serves instead of having in django normal way in admin side object1 ,object2 it will make visible through the name and department we chose now 

#pharmacologist database 

class laboratorist(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address= models.CharField(max_length=50,choices=Addres,default='hargeisa')
    mobile = models.CharField(max_length=20,unique=True)
    test= models.CharField(max_length=50,choices=testo,default='blood')
    status=models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.test)


class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    age=models.IntegerField(default=18)
    address= models.CharField(max_length=50,choices=Addres,default='hargeisa')
    mobile = models.CharField(max_length=20,unique=True)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+"("+self.user.last_name

    class Meta:
        db_table = "patient"






class treatment(models.Model):
    patientid=models.ForeignKey(Patient,on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=100, null=True)
    diagnosis = models.CharField(max_length=100, null=True)
    treatment = models.CharField(max_length=100, null=False, default="nasasho")
    medicne = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now=True)

    @property
    def get_name(self):
        return self.patientid.user.first_name+" "+self.patientid.user.last_name
    @property
    def get_id(self):
        return self.patientid.user.id
    def __str__(self):
        return  self.patientid.user.first_name+" ("+self.diagnosis

    class Meta:
        db_table = "daawada"







class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    doctorName=models.CharField(max_length=40,null=True)
    patientName = models.CharField(max_length=40, null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  self.patientName+" ("+self.doctorName+")"+":"+self.description

    class Meta:
        db_table = "appointment"




class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms=models.CharField(max_length=100,null=True)
    diagnosis=models.CharField(max_length=100,null=True)
    treatment = models.CharField(max_length=100, null=True)
    medicne = models.CharField(max_length=100, null=True)
    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)


    def __str__(self):
        return self.patientName

    class Meta:
        db_table = "discharge"





class massages(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='hospitl')
    message=models.CharField(max_length=500)

    def __str__(self):
        return self.by

    class Meta:
        db_table = "fariimaha"




class khaas(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=50,null=True,default='hospital')
    to=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.CharField(max_length=500)

    def __str__(self):
        return "{} ({})".format(self.by, self.to)

    class meta:
        db_table="khaas"


# class grouping(models.Model):
#     date=models.DateField(auto_now=True)
#     by=models.CharField(max_length=50,null=True,default='hospital')
#     to=models.ManyToManyField(User,null=True,blank=True)
#     message = models.CharField(max_length=500)
#
#     class meta:
#         db_table = "grouping"







    
class shaybaadh(models.Model):
    
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    labaratorist=models.ForeignKey( laboratorist,on_delete=models.CASCADE)
    testname=models.CharField(max_length=50)
    result=models.TextField

    class Meta:
        db_table = "shaybaadh"





class instructions(models.Model):
    caption = models.CharField(max_length=100)
    video = models.FileField(upload_to="instructions/%y")

def __str__(self):
    return  self.cinwaan;











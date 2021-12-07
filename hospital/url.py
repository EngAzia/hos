from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView, LogoutView

# -------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('report', views.report, name="report"),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),
    path('laboratoristclick', views.laboratoristclick_view, name='laboratoristclick'),
    # path('pharmacologist', views.pharmacologist_view ,name='pharmacologist'),

    path('fariimaha',views.fariimaha,name='fariimaha'),

    path('adminsignup', views.admin_signup_view, name="adminsignup"),
    path('doctorsignup', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),
    path('laboratoristsignup', views.laboratorist_signup_view),

    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),
    path('laboratoristlogin', LoginView.as_view(template_name='hospital/laboratoristlogin.html')),

    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('/logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),

    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-report', views.admin_report_view, name='admin-report'),
    path('admin-notice', views.admin_notice_view, name='admin-notice'),
    path('admin_khaas',views.admin_khaas_view,name='admin_khaas'),
    path('doctor_khaas',views.doctor_khaas_view,name='admin_khaas'),

    path('admin-doctor', views.admin_doctor_view, name='admin-doctor'),
    path('admin-laboratorist', views.admin_laboratorist_view, name='admin-laboratorist'),
    path('admin-view-doctor', views.admin_view_doctor_view, name='admin-view-doctor'),
    path('admin-view-laboratorist', views.admin_view_laboratorist_view, name='admin-view-laboratorist'),

    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,
         name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view, name='update-doctor'),
    path('update-laboratorist/<int:pk>', views.update_laboratorist_view, name='update-laboratorist'),
    path('admin-add-doctor', views.admin_add_doctor_view, name='admin-add-doctor'),
    path('admin-add-laboratorist', views.admin_add_laboratorist_view, name='admin-add-laboratorist'),

    path('admin-approve-doctor', views.admin_approve_doctor_view, name='admin-approve-doctor'),
    path('admin-approve-laboratorist', views.admin_approve_laboratorist_view, name='admin-approve-laboratorist'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view, name='approve-doctor'),
    path('approve-laboratorist/<int:pk>', views.approve_laboratorist_view, name='approve-laboratorist'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view, name='reject-doctor'),
    path('reject-laboratorist/<int:pk>', views.reject_laboratorist_view, name='reject-laboratorist'),

    path('admin-view-doctor-specialisation', views.admin_view_doctor_specialisation_view,
         name='admin-view-doctor-specialisation'),

    path('admin-patient', views.admin_patient_view, name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view, name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,
         name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view, name='update-patient'),

    path('admin-add-patient', views.admin_add_patient_view, name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view, name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view, name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view, name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view, name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view, name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view, name='download-pdf'),

    path('admin-appointment', views.admin_appointment_view, name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view, name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view, name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view, name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view, name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view, name='reject-appointment'),
]
# -----for labarotorist related URLS
urlpatterns += [
    # path('laboratorist-dashboard', views.laboratorist_dashboard_view,name='doctor-dashboard'),

    # path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    # path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    # path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    # path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    # path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    # path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    # path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]

# ---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns += [
    path('doctor-dashboard', views.doctor_dashboard_view, name='doctor-dashboard'),
    path('doctorTreatment', views.doctor_treatment_view, name='doctorTreatment'),
    path('doctor-notice/<str:pk>', views.doctor_notice_view, name='doctor-notice'),
    path("patient-state", views.patient_state_veiw, name="patient-state"),

    path('doctor-patient', views.doctor_patient_view, name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view, name='doctor-view-patient'),
    path('doctor-view-discharge-patient', views.doctor_view_discharge_patient_view,
         name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view, name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view, name='doctor-view-appointment'),
    path('doctor-delete-appointment', views.doctor_delete_appointment_view, name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view, name='delete-appointment'),
]

# ---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns += [

    path('patient-dashboard', views.patient_dashboard_view, name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view, name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view, name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view, name='patient-view-appointment'),
    path('patient-discharge', views.patient_discharge_view, name='patient-discharge'),

]



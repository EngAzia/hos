from django.contrib import admin
from .models import *
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json

#begining of admin adminstrations

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user','address','mobile','department','status', 'date_created')
    search_fields = ("mobile", )
    list_filter = ('address', 'department','date_created')


    save_as = True
    save_on_top = True
    change_list_template = 'hospital/change_list_graph.html'

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Doctor.objects.annotate(date=TruncDay("date_created"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
    # search_fields = ["mobile"]
admin.site.register(Doctor, DoctorAdmin)


#end of admin reports



#start of patient registeration

class patientAdmin(admin.ModelAdmin):
    list_display = ('user','age','address','mobile','status', 'date_created')
    search_fields = ["mobile"]
    list_filter = ('address', 'age','date_created')


    save_as = True
    save_on_top = True
    change_list_template = 'hospital/patient_report.html'

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Doctor.objects.annotate(date=TruncDay("date_created"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Patient, patientAdmin)

#end of pateint adminsteration


class laboratoristAdmin(admin.ModelAdmin):
    search_fields = ["mobile"]
admin.site.register(laboratorist, laboratoristAdmin)




class treatmentAdmin(admin.ModelAdmin):
    search_fields = ["patientid"]
admin.site.register(treatment, treatmentAdmin)

class shaybaadhAdmin(admin.ModelAdmin):
    pass
admin.site.register(shaybaadh, shaybaadhAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)

class massagesAdmin(admin.ModelAdmin):
	pass
admin.site.register(massages,massagesAdmin)





class instructionAdmin(admin.ModelAdmin):
    pass
admin.site.register(instructions,instructionAdmin)


class khaasadmin(admin.ModelAdmin):
    pass
admin.site.register(khaas,khaasadmin)
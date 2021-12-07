import django_filters
from .models import Doctor

class DoctorFilter(django_filters.FilterSet):
    class Meta:

        model = Doctor
        fields = ['user','department']
        exclude=[]
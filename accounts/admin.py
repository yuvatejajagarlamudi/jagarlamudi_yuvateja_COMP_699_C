from django.contrib import admin
from .models import Resident, MunicipalStaff, AdminProfile

admin.site.register(Resident)
admin.site.register(MunicipalStaff)
admin.site.register(AdminProfile)

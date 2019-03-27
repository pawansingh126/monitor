from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Owners)
admin.site.register(models.OwnerTypes)
admin.site.register(models.UnknownEntries)
admin.site.register(models.Vehicles)
admin.site.register(models.VehicleTypes)
admin.site.register(models.MediaForUnknownVehicles)
admin.site.register(models.EmpVehMap)
admin.site.register(models.Attendance)
admin.site.register(models.UserRoles)
admin.site.register(models.Users)

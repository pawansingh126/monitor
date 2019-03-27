from django.db import models

# Create your models here.

# VEHICLE_TYPES = (
#     (0, 'Bike'),
#     (1, 'Small Car'),
#     (2, 'Big Car'),
#     (3, 'Pantry Pick Up Truck'),
#     (4, 'Unassigned'),
# )

# OWNER_TYPES = (
#     (0, 'Employee'),
#     (1, 'Visitor'),
#     (2, 'Unknown'),
# )

def imageFile(instance, filename):
    return '/'.join(['images', str(instance.id), filename])

class VehicleTypes(models.Model):

    vtype = models.CharField(max_length=30, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vtype


class Vehicles(models.Model):

    vehicle_number = models.CharField(max_length=15, unique=True)
    vehicle_type = models.ForeignKey(VehicleTypes, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehicle_number


class OwnerTypes(models.Model):

    owner_type = models.CharField(max_length=30, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner_type


class Owners(models.Model):

    owner_id = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
    ph_num = models.CharField(max_length=15)
    active = models.BooleanField(default=True)
    owner_type = models.ForeignKey(OwnerTypes, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class EmpVehMap(models.Model):

    owner = models.ForeignKey(Owners, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class Attendance(models.Model):

    vehicle_map = models.ForeignKey(EmpVehMap, on_delete=models.CASCADE)
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(default='')
    active = models.BooleanField(default=True)
    note = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class UnknownEntries(models.Model):

    vehicle_number = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=15)
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(default='')
    active = models.BooleanField(default=True)
    note = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehicle_number


class MediaForUnknownVehicles(models.Model):

    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=imageFile, max_length=254, blank=True, null=True)
    unknown_entry = models.ForeignKey(UnknownEntries, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class UserRoles(models.Model):

    name = models.CharField(max_length=20)
    code = models.IntegerField(default=0)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Users(models.Model):

    emp_id = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
    role = models.ForeignKey(UserRoles, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class LogTypes(models.Model):

    log_type = models.CharField(max_length=30)
    description = models.CharField(max_length=200)


class Logging(models.Model):

    log_type = models.ForeignKey(LogTypes, on_delete=models.CASCADE)
    log_context = models.CharField(max_length=300)
    log_time = models.DateTimeField(auto_now_add=True)

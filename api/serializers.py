from rest_framework import serializers
from . models import *


class VehicleTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleTypes
        fields = '__all__'


class VehiclesSerializer(serializers.ModelSerializer):
    vehicle_type = VehicleTypesSerializer(read_only=True)

    class Meta:
        model = Vehicles
        fields = '__all__'


class OwnerTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = OwnerTypes
        fields = '__all__'


class OwnersSerializer(serializers.ModelSerializer):
    owner_type = OwnerTypesSerializer()

    class Meta:
        model = Owners
        fields = '__all__'


class EmpVehMapSerializer(serializers.ModelSerializer):
    owner = OwnersSerializer()
    vehicle = VehiclesSerializer()

    class Meta:
        model = EmpVehMap
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    vehicle_map = EmpVehMapSerializer()

    class Meta:
        model = Attendance
        fields = '__all__'


class UnknownEntriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnknownEntries
        fields = '__all__'


class MediaForUnknownVehiclesSerializer(serializers.ModelSerializer):
    unknown_entry = UnknownEntriesSerializer()

    class Meta:
        model = MediaForUnknownVehicles
        fields = '__all__'


class UserRolesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRoles
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    role = UserRolesSerializer()

    class Meta:
        model = Users
        fields = '__all__'

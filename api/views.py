import datetime

from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . models import *
from . serializers import *

# Create your views here.

res = dict(status=0, data=dict())

def get_vehicle_type(vt, return_object=False):
    if vt:
        if isinstance(vt, str):
            try:
                vtype = VehicleTypes.objects.get(vtype=vt)
            except:
                return {}
        elif isinstance(vt, int):
            try:
                vtype = VehicleTypes.objects.get(vt)
            except:
                return {}
        if return_object:
            return vtype
        return VehicleTypesSerializer(vtype).data
    return {}

def get_vehicle(vehicle_number='', return_object=False):
    if vehicle_number:
        if isinstance(vehicle_number, int):
            try:
                vehicle = Vehicles.objects.get(vehicle_number)
            except:
                return {}
        else:
            try:
                vehicle = Vehicles.objects.get(vehicle_number=vehicle_number)
            except:
                return {}
        if return_object:
            return vehicle
        return VehiclesSerializer(vehicle).data
    return {}

def get_owner_type(ot, return_object=False):
    if ot:
        if isinstance(ot, str):
            try:
                otype = OwnerTypes.objects.get(owner_type=vt)
            except:
                return {}
        elif isinstance(ot, int):
            try:
                otype = VehicleTypes.objects.get(ot)
            except:
                return {}
        if return_object:
            return otype
        return OwnerTypesSerializer(otype).data
    return {}

def get_owner(owner, return_object=False):
    if owner:
        pass


def find_active_unknown_entry(vehicle_number, return_object=False):
    entries = UnknownEntries.objects.filter(
        vehicle_number=vehicle_number, active=True
    ).order_by('-created_date')
    if entries:
        if return_object:
            return entries[0]
        return UnknownEntriesSerializer(entries[0]).data
    return {}

def find_active_attendance(vehicle_number, return_object=False):
    attendances = Attendance.objects.filter(
        vehicle_number=vehicle_number, active=True
    ).order_by('-created_date')
    if attendances:
        if return_object:
            return attendances[0]
        return AttendanceSerializer(attendances[0]).data
    return {}

def get_vehicle_map(vehicle, return_object=False):
    if isinstance(vehicle, str):
        vehicle = get_vehicle(vehicle)
        if vehicle:
            vehicle_id = vehicle.get('id')
    elif isinstance(vehicle, int):
        vehicle_id = vehicle
    elif isinstance(vehicle, Vehicles):
        vehicle_id = vehicle.id
    maps = EmpVehMap.objects.filter(
        vehicle_number=vehicle_id, active=True
    ).order_by('-created_date')
    if maps:
        if return_object:
            return maps[0]
        return EmpVehMapSerializer(maps[0]).data
    return {}

def make_unknown_entry(request):
    return UnknownEntries(**request.data)

def add_reference_media(request, unknown_entry, return_object=False):
    image = request.data.get('file', None)
    if image:
        if isinstance(unknown_entry, UnknownEntries):
            media = MediaForUnknownVehicles(
                image=image, name=image.name, unknown_entry=unknown_entry)
            media.save()
            if return_object:
                return media
            return MediaForUnknownVehiclesSerializer(media).data
    return {}

def mark_attendace(vehicle_num, vehicle_map):
    attendance = find_active_attendance(vehicle_num)
    if attendance:
        attendance.out_time = datetime.datetime.now()
    else:
        attendance = Attendance(vehicle_map=vehicle_map)
    return attendance

class vehicleTypes(APIView):

    def get(self, request):
        vt  = VehicleTypes.objects.all()
        serializer = VehicleTypesSerializer(vt, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            vt = VehicleTypes(**request.data)
            vt.save()
            res["data"] = VehicleTypesSerializer(vt).data
            res["status"] = 1
        except Exception as e:
            res['message'] = str(e)
        return Response(res)

class vehicles(APIView):

    def get(self, request, vehicle=''):
        if vehicle:
            res = get_vehicle(vehicle)
        else:
            vehicles  = Vehicles.objects.all()
            serializer = VehiclesSerializer(vehicles, many=True)
            res["count"] = len(vehicles),
            res["data"] = serializer.data
            res["status"] = 1
        return Response(res)

    def post(self, request):
        vehicle_type = request.data.get('vehicle_type')
        if vehicle_type:
            try:
                vt = get_vehicle_type(vehicle_type, True)
                if vt:
                    request.data['vehicle_type'] = vt
                else:
                    raise 'Vehicle Type not found!'
            except:
                res["messages"] = 'Vehicle Type not found!'
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        try:
            vehicle = Vehicles(**request.data)
            vehicle.save()
            serializer = VehiclesSerializer(vehicle)
            res["data"] = serializer.data
            res["status"] = 1
            return Response(res)
        except Exception as e:
            res["message"] = str(e)
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class markEntry(APIView):

    def get(self, request):
        pass

    def post(self, request):
        res = dict(message='', status=0)
        vehicle_num = request.data.get('vehicle_number')
        vehicle_type = request.data.get('vehicle_type')
        vehicle = get_vehicle(vehicle_num, return_object=True)
        unknown_entry = find_active_unknown_entry(
            vehicle_num, return_object=True)
        vehicle_map = get_vehicle_map(vehicle_num, return_object=True)
        if vehicle:
            if vehicle_map:
                attendance = mark_attendace(vehicle_num, vehicle_map)
                if not vehicle_type:
                    attendance.note = 'Model unable to detect vehicle type.'
                elif vehicle_type != vehicle.vehicle_type:
                    attendance.note = 'Found vehicle type mismatch.'
                attendance.save()
                res['message'] = "Attendance Marked!"
                res['status'] = 1
                res['data'] = AttendanceSerializer(attendance).data
            else:
                request.data['note'] = 'Vehicle mapping not found in records.'
                unknown_entry = make_unknown_entry(request)
                unknown_entry.save()
                res['message'] = "Vehicle map not found. Unknown entry marked."
                res['status'] = 2
                res['data'] = UnknownEntriesSerializer(unknown_entry).data

        else:
            if unknown_entry:
                unknown_entry.out_time = datetime.datetime.now()
            else:
                unknown_entry = make_unknown_entry(request)
            unknown_entry.save()
            res['message'] = "Unknown entry marked!"
            res['status'] = 3
            res['data'] = UnknownEntriesSerializer(unknown_entry).data
        return Response(res)


class ownerTypes(APIView):

    def get(self, request):
        ot  = OwnerTypes.objects.all()
        serializer = OwnerTypesSerializer(ot, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            ot = OwnerTypes(**request.data)
            ot.save()
            res["data"] = OwnerTypesSerializer(ot).data
            res["status"] = 1
        except Exception as e:
            res['message'] = str(e)
        return Response(res)


class owners(APIView):

    def get(self, request):
        owner  = Owners.objects.all()
        serializer = OwnersSerializer(owner, many=True)
        return Response(serializer.data)

    def post(self, request):
        owner_type = request.data.get('vehicle_type')
        if owner_type:
            try:
                ot = get_owner_type(owner_type, True)
                if ot:
                    request.data['owner_type'] = ot
                else:
                    raise 'Owner Type not found!'
            except:
                res["messages"] = 'Owner Type not found!'
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        try:
            owner = Vehicles(**request.data)
            owner.save()
            serializer = OwnersSerializer(owner)
            res["data"] = serializer.data
            res["status"] = 1
            return Response(res)
        except Exception as e:
            res["message"] = str(e)
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class vehicleMap(APIView):

    def get(self, request):
        evm  = EmpVehMap.objects.all()
        serializer = EmpVehMapSerializer(evm, many=True)
        return Response(serializer.data)

    def post(self, request):
        owner = request.data.get('owner')
        vehicle = request.data.get('vehicle')
        if owner and vehicle:
            try:
                ot = get_owner(owner, True)
                if ot:
                    request.data['owner_type'] = ot
                else:
                    raise 'Owner Type not found!'
            except:
                res["messages"] = 'Owner Type not found!'
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        try:
            owner = Vehicles(**request.data)
            owner.save()
            serializer = OwnersSerializer(owner)
            res["data"] = serializer.data
            res["status"] = 1
            return Response(res)
        except Exception as e:
            res["message"] = str(e)
            return Response(res, status=status.HTTP_400_BAD_REQUEST)



class attendance(APIView):

    def get(self, request):
        registries  = Attendance.objects.all()
        serializer = VehiclesSerializer(registries, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass


class unknownEntries(APIView):

    def get(self, request):
        ue  = UnknownEntries.objects.all()
        serializer = UnknownEntriesSerializer(ue, many=True)
        return Response(serializer.data)


class mediaForUnknownVehicles(APIView):

    def get(self, request):
        muv  = MediaForUnknownVehicles.objects.all()
        serializer = MediaForUnknownVehiclesSerializer(muv, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            unknown_entry = UnknownEntries.objects.get(request.data.get(
                'unknown_entry'))
            media = MediaForUnknownVehicles(unknown_entry=unknown_entry)
            media.file = request.data.get('file')
            media.save()
            res['data'] = MediaForUnknownVehiclesSerializer(media).data
            res['status'] = 1
            return Response(res)
        except Exception as e:
            res['message'] = str(e)
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


class usersList(APIView):

    def get(self, request):
        users  = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)


class usersRolesList(APIView):

    def get(self, request):
        users  = UserRoles.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)

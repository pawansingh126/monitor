"""monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, re_path
from . import views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Vehicle Monitoring API!!!')

urlpatterns = [
    url(r'^$', schema_view),
    url(r'^vehicle-types$', views.vehicleTypes.as_view(), name='api_vehicle_types'),
    url(r'^vehicles$', views.vehicles.as_view(), name='api_vehicles'),
    url(r'^vehicles/(?P<vehicle>\w+)', views.vehicles.as_view(), name='api_vehicle'),
    url(r'^owner-types$', views.usersList.as_view(), name='api_owner_types'),
    url(r'^owners$', views.usersList.as_view(), name='api_'),
    url(r'^users$', views.usersList.as_view(), name='api_'),
    url(r'^users$', views.usersList.as_view(), name='api_'),
    url(r'^users$', views.usersList.as_view(), name='api_'),
    url(r'^users$', views.usersList.as_view(), name='api_'),
    url(r'^users$', views.usersList.as_view(), name='api_'),
]

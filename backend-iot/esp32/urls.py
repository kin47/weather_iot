from django.urls import path
from . import views

app_name = 'esp32'

urlpatterns = [
    path('data', view=views.DataDrive.as_view(), name='esp32-data'),
]

from django.urls import path
from . import views

app_name = 'disease_detection'

urlpatterns = [
    path('', view=views.DiseaseDetection.as_view(), name='detect'),
]

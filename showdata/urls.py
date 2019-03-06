
from django.urls import path
from . import views

app_name = 'showdata'

urlpatterns = [
    # GET / 
    path('', views.index, name='index'), 
]
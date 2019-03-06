from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from showdata.serializers import EntrySerializer
from showdata.models import  Specie, Kingdom, Entry


# Create your views here.

def index(request):
    return HttpResponse("Indice não implementado.")


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all().order_by('access_id')
    serializer_class = EntrySerializer
from django.db import models
from django.urls import reverse

# Create your models here.

class Kingdom(models.Model):
    label = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('kingdom_detail', args=[str(self.label)])    


class Specie(models.Model):
    label = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('specie_detail', args=[str(self.label)])    


class Entry(models.Model):
    access_id = models.CharField(max_length=20, verbose_name='access id', unique=True, null=False, blank=False)
    kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE)
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
    sequence = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.access_id

    def get_absolute_url(self):
        return reverse('entry_detail', args=[str(self.access_id)])    

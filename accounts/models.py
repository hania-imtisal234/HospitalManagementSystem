from time import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
#Create your models here.
class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default = False)
    is_doctor = models.BooleanField(default=False)

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255) 
    email = models.EmailField(unique=True) 
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    specialization = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return self.full_name

class PatientProfile(models.Model):
     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
     full_name = models.CharField(max_length=255) 
     email = models.EmailField(unique=True) 
     phone_number = models.CharField(max_length=15, blank=True, null=True)  
     date_of_birth = models.DateField()
     GENDERS = [ 
         ('male', 'Male'),
         ('female', 'Female'),
     ]
     gender = models.CharField(max_length=100, choices= GENDERS)  
     created_at = models.DateTimeField(auto_now_add=True)  
     updated_at = models.DateTimeField(auto_now=True) 

    
     def __str__(self):
         return self.full_name



from time import timezone
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# #Create your models here.
# class CustomUser(AbstractUser):
#     is_admin = models.BooleanField(default = False)
#     is_doctor = models.BooleanField(default=False)

# class DoctorProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=255) 
#     email = models.EmailField(unique=True) 
#     phone_number = models.CharField(max_length=15, blank=True, null=True)  
#     specialization = models.CharField(max_length=100)  
#     created_at = models.DateTimeField(auto_now_add=True)  
#     updated_at = models.DateTimeField(auto_now=True) 
    
#     def __str__(self):
#         return self.full_name

# class PatientProfile(models.Model):
#      user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#      full_name = models.CharField(max_length=255) 
#      email = models.EmailField(unique=True) 
#      phone_number = models.CharField(max_length=15, blank=True, null=True)  
#      date_of_birth = models.DateField()
#      GENDERS = [ 
#          ('male', 'Male'),
#          ('female', 'Female'),
#      ]
#      gender = models.CharField(max_length=100, choices= GENDERS)  
#      created_at = models.DateTimeField(auto_now_add=True)  
#      updated_at = models.DateTimeField(auto_now=True) 

    
#      def __str__(self):
#          return self.full_name


from django.db import models
from django.contrib.auth.models import AbstractUser

from patients.models import Patient
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # Define roles as choices
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin')
    username = models.CharField(max_length=150, unique=True, blank=True, null=True) 
    full_name = models.CharField(max_length=255 , blank= True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDERS = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=100, choices=GENDERS, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    def is_admin(self):
        return self.role == 'admin'

    def is_doctor(self):
        return self.role == 'doctor'

    def is_patient(self):
        return self.role == 'patient'
    

class Appointment(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_appointments')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_appointments')
    scheduled_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def clean(self):
    #     # Ensure that the doctor is a user with a doctor role
    #     if self.doctor.role != 'doctor':
    #         raise ValidationError(_('The selected doctor must have the role of "doctor".'))

    #     # Ensure that the patient is a user with a patient role
    #     if self.patient.role != 'patient':
    #         raise ValidationError(_('The selected patient must have the role of "patient".'))

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.full_name} for {self.patient.full_name} on {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"

    # def save(self, *args, **kwargs):
    #     # Perform the validation before saving
    #     self.clean()
    #     super().save(*args, **kwargs)

class MedicalRecord(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='medical_records_as_doctor')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='medical_records_as_patient')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='medical_records')
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)
    report = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical Record for {self.diagnosis} - {self.created_at.strftime('%Y-%m-%d')}"

    def is_doctor(self):
        return self.role == 'doctor'

    def is_patient(self):
        return self.role == 'patient'
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.forms import LoginForm, DoctorProfileForm, CreateRecordForm, PatientProfileForm
from django.urls import reverse
from .models import CustomUser, Appointment, MedicalRecord
from django.views.decorators.cache import cache_control

def user_login(request):
    """
    Handle user login. If the request method is POST, authenticate the user with
    provided username and password. On successful authentication, redirect to the
    appropriate dashboard based on user role. If authentication fails, re-render
    the login page with an error message.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin')
                elif user.is_admin():
                    return redirect('admin_dashboard')
                elif user.is_doctor():
                    return redirect(reverse('doctor_dashboard') + f'?user_id={user.id}')
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def doctor_dashboard(request, doctor_id=None):
    """
    Display the dashboard for a specific doctor. If a doctor_id is provided or
    in the query parameters, retrieve and display the doctor's information along
    with their appointments and associated medical records.
    """
    user_id = doctor_id if doctor_id else request.GET.get('user_id')
    if user_id:
        try:
            doctor_user = get_object_or_404(CustomUser, id=user_id)
            appointment_info = Appointment.objects.filter(doctor=doctor_user)
            appointments_with_records = []
            for appointment in appointment_info:
                records = MedicalRecord.objects.filter(appointment=appointment)
                appointments_with_records.append({
                    'appointment': appointment,
                    'records': records
                })
        except CustomUser.DoesNotExist:
            return redirect('user_login')
    return render(request, 'doctors/doctor-info.html', {
        'doctor_user': doctor_user,
        'appointments_with_records': appointments_with_records,
    })

def record_list(request):
    """
    List medical records for a specific appointment. Retrieve records based on
    appointment_id, patient_id, and doctor_id from POST data or session.
    """
    appointment_id = request.POST.get('appointment_id') or request.session.get('appointment_id')
    patient_id = request.POST.get('patient_id') or request.session.get('patient_id')
    doctor_id = request.POST.get('doctor_id') or request.session.get('doctor_id')

    records = MedicalRecord.objects.filter(appointment_id=appointment_id)
    recordform = CreateRecordForm()

    record_lists = {
        'appointment_id': appointment_id,
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'records': records
    }

    return render(request, 'patients/med-records.html', {
        'record_list': record_lists,
        'record_form': recordform,
    })

def records(request):
    """
    Create or update medical records based on POST data. The action is determined
    by the 'type' parameter ('create' or 'update'). The appointment, patient, and
    doctor information is used to save or update records.
    """
    if request.method == 'POST':
        records_form = CreateRecordForm(request.POST)
        if records_form.is_valid():
            appointment_id = request.POST.get('appointment_id')
            patient_id = request.POST.get('patient_id')
            doctor_id = request.POST.get('doctor_id')
            type_edit = request.POST.get('type')
            appointment = Appointment.objects.get(id=appointment_id)
            doctor = CustomUser.objects.get(id=doctor_id)
            patient = CustomUser.objects.get(id=patient_id)
            try:
                if type_edit == 'create':
                    MedicalRecord.objects.create(
                        diagnosis=records_form.cleaned_data['diagnosis'],
                        treatment=records_form.cleaned_data['treatment'],
                        notes=records_form.cleaned_data['notes'],
                        report=records_form.cleaned_data['report'],
                        appointment=appointment,
                        patient=patient,
                        doctor=doctor
                    )
                elif type_edit == 'update':
                    MedicalRecord.objects.filter(appointment=appointment).update(
                        diagnosis=records_form.cleaned_data['diagnosis'],
                        treatment=records_form.cleaned_data['treatment'],
                        notes=records_form.cleaned_data['notes'],
                        report=records_form.cleaned_data['report'],
                    )
                request.session['appointment_id'] = appointment_id
                request.session['patient_id'] = patient_id
                request.session['doctor_id'] = doctor_id

                return redirect('record_list')
            except Exception as e:
                print("Error:", e)
    return render(request, 'patients/med-records.html')

def admin_required(user):
    """
    Check if the user is authenticated and has admin privileges.
    """
    return user.is_authenticated and user.is_admin()

@login_required
@user_passes_test(admin_required)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    """
    Render the admin dashboard. Accessible only to users with admin privileges.
    """
    return render(request, 'accounts/admin.html')

@login_required
def user_logout(request):
    """
    Log out the user and redirect to the login page.
    """
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(admin_required)
def doctor_list_view(request):
    """
    Display a list of doctors, with optional search and specialization filters.
    """
    search_query = request.GET.get('search', '')
    specialization_filter = request.GET.get('specialization', '')
    doctors = CustomUser.objects.filter(role='doctor')
    
    if search_query:
        doctors = doctors.filter(full_name__icontains=search_query)

    if specialization_filter:
        doctors = doctors.filter(specialization__icontains=specialization_filter)
    
    context = {
        'list_name': "Doctor's List",
        'doctors': doctors,
        'search_query': search_query,
        'specialization_filter': specialization_filter,
    }
    
    return render(request, 'accounts/doctor_list.html', context)

@login_required
@user_passes_test(admin_required)
def doctor_detail_view(request, pk):
    """
    Display detailed information about a specific doctor.
    """
    doctor = get_object_or_404(CustomUser, pk=pk, role='doctor')
    return render(request, 'accounts/doctor_detail.html', {'doctor': doctor})

@login_required
@user_passes_test(admin_required)
def create_update_doctor_view(request, pk=None):
    """
    Create or update a doctor's profile. If pk is provided, update the existing
    doctor's profile; otherwise, create a new one.
    """
    if pk:
        doctor = get_object_or_404(CustomUser, pk=pk, role='doctor')
    else:
        doctor = None
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor_profile = form.save(commit=False)
            doctor_profile.role = 'doctor'
            doctor_profile.user = request.user
            doctor_profile.save()
            return redirect('doctor_list_view')
    else:
        form = DoctorProfileForm(instance=doctor)
    
    return render(request, 'accounts/doctor_form.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def delete_doctor_view(request, pk):
    """
    Delete a doctor's profile. Confirm deletion with a POST request.
    """
    doctor = get_object_or_404(CustomUser, pk=pk, role='doctor')
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list_view')
    return render(request, 'accounts/doctor_confirm_delete.html', {'doctor': doctor})

@login_required
@user_passes_test(admin_required)
def patient_list_view(request):
    """
    Display a list of patients, with optional search and gender filters.
    """
    search_query = request.GET.get('search', '')
    gender_filter = request.GET.get('gender', '')
    
    patients = CustomUser.objects.filter(role='patient')
    
    if search_query:
        patients = patients.filter(full_name__icontains=search_query)
    
    if gender_filter:
        patients = patients.filter(gender__icontains=gender_filter)
    
    context = {
        'list_name': "Patient's List",
        'patients': patients,
        'search_query': search_query,
        'gender_filter': gender_filter,
    }
    return render(request, 'patients/patient_list.html', context)

@login_required
@user_passes_test(admin_required)
def patient_detail_view(request, pk):
    """
    Display detailed information about a specific patient.
    """
    patient = get_object_or_404(CustomUser, pk=pk, role='patient')
    return render(request, 'patients/patient_detail.html', {'patient': patient})

@login_required
@user_passes_test(admin_required)
def create_update_patient_view(request, pk=None):
    """
    Create or update a patient's profile. If pk is provided, update the existing
    patient's profile; otherwise, create a new one.
    """
    if pk:
        patient = get_object_or_404(CustomUser, pk=pk, role='patient')
    else:
        patient = None
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            patient_profile = form.save(commit=False)
            patient_profile.role = 'patient'
            patient_profile.user = request.user
            patient_profile.save()
            return redirect('patient_list_view')
    else:
        form = PatientProfileForm(instance=patient)
    
    return render(request, 'patients/patient_form.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def delete_patient_view(request, pk):
    """
    Delete a patient's profile. Confirm deletion with a POST request.
    """
    patient = get_object_or_404(CustomUser, pk=pk, role='patient')
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list_view')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})

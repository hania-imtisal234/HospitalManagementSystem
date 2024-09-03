# from django.shortcuts import get_object_or_404, redirect, render
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required, user_passes_test
# from accounts.forms import LoginForm
# # from .models import DoctorProfile, PatientProfile

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)  
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 if user.is_superuser:
#                     return redirect('/admin')
#                 elif user.is_admin:
#                     return redirect('admin_dashboard')
#                 elif user.is_doctor:
#                     return redirect('doctor_dashboard')
#             else:
#                 return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
#     else:
#         form = LoginForm()

#     return render(request, 'accounts/login.html', {'form': form})


# @login_required
# def doctor_dashboard(request):
#     return render(request, 'accounts/doctor.html')

# @login_required
# def admin_dashboard(request):
#     return render(request, 'accounts/admin.html')


# def admin_required(user):
#     return user.is_authenticated and user.is_admin


# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('login') 

# @login_required
# @user_passes_test(admin_required)
# def doctor_list_view(request):
#     search_query = request.GET.get('search', '')
#     specialization_filter = request.GET.get('specialization', '')
    
#     doctors = DoctorProfile.objects.all()
    
#     if search_query:
#         doctors = doctors.filter(full_name__icontains=search_query)
    
#     if specialization_filter:
#         doctors = doctors.filter(specialization=specialization_filter)
    
#     context = {
#         'doctors': doctors,
#         'search_query': search_query,
#         'specialization_filter': specialization_filter,
#     }
#     return render(request, 'accounts/doctor_list.html', context)

# @login_required
# @user_passes_test(admin_required)
# def doctor_detail_view(request, pk):
#     doctor = get_object_or_404(DoctorProfile, pk=pk)
#     return render(request, 'accounts/doctor_detail.html', {'doctor': doctor})

# @login_required
# @user_passes_test(admin_required)
# def create_update_doctor_view(request, pk=None):
#     if pk:
#         doctor = get_object_or_404(DoctorProfile, pk=pk)
#     else:
#         doctor = None
    
#     if request.method == 'POST':
#         form = DoctorProfileForm(request.POST, instance=doctor)
#         if form.is_valid():
#             doctor_profile = form.save(commit=False)
#             doctor_profile.user = request.user
#             form.save()
#             return redirect('doctor_list_view')
#     else:
#         form = DoctorProfileForm(instance=doctor)
    
#     return render(request, 'accounts/doctor_form.html', {'form': form})

# @login_required
# @user_passes_test(admin_required)
# def delete_doctor_view(request, pk):
#     doctor = get_object_or_404(DoctorProfile, pk=pk)
#     if request.method == 'POST':
#         doctor.delete()
#         return redirect('doctor_list_view')
#     return render(request, 'accounts/doctor_confirm_delete.html', {'doctor': doctor})

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.forms import LoginForm, DoctorProfileForm, CreateRecordForm  # Import the DoctorProfileForm
from django.urls import reverse

# from database import appointments
from .models import CustomUser, Appointment, MedicalRecord  # Import the CustomUser model

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(username, password)
            print(user)
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
def doctor_dashboard(request):
    user_id = request.GET.get('user_id')
    # print(user_id)
    user = None
    if user_id:
        try:
            doctor_user = get_object_or_404(CustomUser, id=user_id)
            print("User object is", doctor_user)
            appointment_info = Appointment.objects.filter(doctor=doctor_user)
            print(appointment_info)
            appointments_with_records = []
            for appointment in appointment_info:
                records = MedicalRecord.objects.filter(appointment=appointment)
                # print('In doctor dashnoard')
                # print(records)
                appointments_with_records.append({
                    'appointment': appointment,
                    'records': records
                })
        except CustomUser.DoesNotExist:
            return redirect('user_login')
    # if request.method == 'POST':
    #    userform = LoginForm(request.POST)

    # if userform.is_valid():
    #     print(userform.cleaned_data)
    return render(request, 'doctors/doctor-info.html',{
        'doctor_user' : doctor_user,
        'appointments_with_records': appointments_with_records,
    })

def record_list(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        records = MedicalRecord.objects.filter(appointment_id=appointment_id)
        recordform = CreateRecordForm()

        # records = request.POST.get('records')
        # print(appointment_id, doctor_id, patient_id)

        record_lists = {
            'appointment_id': appointment_id,
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'records': records
        }
        # print('in record_list view')
        # print(record_lists['records'])

    return render(request, 'patients/med-records.html',{
        'record_list': record_lists,
        "record_form": recordform,

    })

def records(request):
    if request.method == 'POST':
        records_form = CreateRecordForm(request.POST)
        if records_form.is_valid():
            print(records_form.cleaned_data)
            appointment_id = request.POST.get('appointment_id')
            patient_id = request.POST.get('patient_id')
            doctor_id = request.POST.get('doctor_id')
            type_edit = request.POST.get('type')
            print(patient_id, appointment_id, doctor_id)
            print(type_edit)
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
                return redirect('patient-medical-records')
            except:
                print("Error")

    return redirect('doctor-dashboard')
@login_required
def admin_dashboard(request):
    return render(request, 'accounts/admin.html')

def admin_required(user):
    return user.is_authenticated and user.is_admin()

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(admin_required)
def doctor_list_view(request):
    search_query = request.GET.get('search', '')
    specialization_filter = request.GET.get('specialization', '')
    
    doctors = CustomUser.objects.filter(role='doctor')
    
    if search_query:
        doctors = doctors.filter(full_name__icontains=search_query)
    
    if specialization_filter:
        doctors = doctors.filter(specialization__icontains=specialization_filter)
    
    context = {
        'doctors': doctors,
        'search_query': search_query,
        'specialization_filter': specialization_filter,
    }
    return render(request, 'accounts/doctor_list.html', context)

@login_required
@user_passes_test(admin_required)
def doctor_detail_view(request, pk):
    doctor = get_object_or_404(CustomUser, pk=pk, role='doctor')
    return render(request, 'accounts/doctor_detail.html', {'doctor': doctor})

@login_required
@user_passes_test(admin_required)
def create_update_doctor_view(request, pk=None):
    if pk:
        doctor = get_object_or_404(CustomUser, pk=pk, role='doctor')
    else:
        doctor = None
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor_profile = form.save(commit=False)
            # Optionally, set any additional attributes
            form.save()
            return redirect('doctor_list_view')
    else:
        form = DoctorProfileForm(instance=doctor)
    
    return render(request, 'accounts/doctor_form.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def delete_doctor_view(request, pk):
    doctor = get_object_or_404(CustomUser, pk=pk, role='doctor')
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list_view')
    return render(request, 'accounts/doctor_confirm_delete.html', {'doctor': doctor})


# @login_required
# @user_passes_test(admin_required)
# def patient_list_view(request):
#     search_query = request.GET.get('search', '')
#     gender_filter = request.GET.get('gender', '')
    
#     patients = CustomUser.objects.filter(role='patient')
    
#     if search_query:
#         patients = patients.filter(full_name__icontains=search_query)
    
#     if gender_filter:
#         patients = patients.filter(gender__icontains=gender_filter)
    
#     context = {
#         'patients': patients,
#         'search_query': search_query,
#         'gender_filter': gender_filter,
#     }
#     return render(request, 'accounts/doctor_list.html', context)
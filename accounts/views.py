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
from accounts.forms import LoginForm, DoctorProfileForm, PatientProfileForm
from .models import CustomUser 

def user_login(request):
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
                    return redirect('doctor_dashboard')
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def doctor_dashboard(request):
    return render(request, 'accounts/doctor.html')

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
        'list_name': "Doctor's List",
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
            doctor_profile.role = 'doctor' 
            doctor_profile.user = request.user
            doctor_profile.save()
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


@login_required
@user_passes_test(admin_required)
def patient_list_view(request):
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
    patient = get_object_or_404(CustomUser, pk=pk, role='patient')
    return render(request, 'patients/patient_detail.html', {'patient': patient})

@login_required
@user_passes_test(admin_required)
def create_update_patient_view(request, pk=None):
    if pk:
        patient = get_object_or_404(CustomUser, pk=pk, role='patient')
    else:
        patient = None
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            patient_profile = form.save(commit=False)
            form.save()
            return redirect('patient_list_view')
    else:
        form = PatientProfileForm(instance=patient)
    
    return render(request, 'patients/patient_form.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def delete_patient_view(request, pk):
    patient = get_object_or_404(CustomUser, pk=pk, role='patient')
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list_view')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.forms import DoctorProfileForm, LoginForm
from .models import DoctorProfile, PatientProfile

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
                elif user.is_admin:
                    return redirect('admin_dashboard')
                elif user.is_doctor:
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
    return user.is_authenticated and user.is_admin


@login_required
def user_logout(request):
    logout(request)
    return redirect('login') 

@login_required
@user_passes_test(admin_required)
def doctor_list_view(request):
    search_query = request.GET.get('search', '')
    specialization_filter = request.GET.get('specialization', '')
    
    doctors = DoctorProfile.objects.all()
    
    if search_query:
        doctors = doctors.filter(full_name__icontains=search_query)
    
    if specialization_filter:
        doctors = doctors.filter(specialization=specialization_filter)
    
    context = {
        'doctors': doctors,
        'search_query': search_query,
        'specialization_filter': specialization_filter,
    }
    return render(request, 'accounts/doctor_list.html', context)

@login_required
@user_passes_test(admin_required)
def doctor_detail_view(request, pk):
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    return render(request, 'accounts/doctor_detail.html', {'doctor': doctor})

@login_required
@user_passes_test(admin_required)
def create_update_doctor_view(request, pk=None):
    if pk:
        doctor = get_object_or_404(DoctorProfile, pk=pk)
    else:
        doctor = None
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor_profile = form.save(commit=False)
            doctor_profile.user = request.user
            form.save()
            return redirect('doctor_list_view')
    else:
        form = DoctorProfileForm(instance=doctor)
    
    return render(request, 'accounts/doctor_form.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def delete_doctor_view(request, pk):
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list_view')
    return render(request, 'accounts/doctor_confirm_delete.html', {'doctor': doctor})




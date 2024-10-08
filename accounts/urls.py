
from django.urls import path
from django.urls import path

from .views import (
    admin_dashboard,
    create_update_doctor_view,
    delete_doctor_view,
    doctor_detail_view,
    doctor_list_view,
    user_login,
    doctor_dashboard,
    user_logout,
    record_list,
    records,
    create_update_patient_view,
    delete_patient_view,
    patient_detail_view,
    patient_list_view
)


urlpatterns = [
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('doctor-dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('doctor-dashboard/<int:doctor_id>/', doctor_dashboard, name='doctor_dashboard_with_id'),
    path('patient-medical-records/', record_list, name='record_list' ),
    path('record/', records, name='records'),

    path('admin-dashoard/', admin_dashboard, name= "admin_dashboard"),
    path('doctors/', doctor_list_view, name='doctor_list_view'),
    path('doctors/<int:pk>/', doctor_detail_view, name='doctor_detail_view'),
    path('doctors/create/', create_update_doctor_view, name='create_doctor_view'),
    path('doctors/update/<int:pk>/', create_update_doctor_view, name='update_doctor_view'),
    path('doctors/delete/<int:pk>/', delete_doctor_view, name='delete_doctor_view'),
    
    #Patient URL:
    path('patients/', patient_list_view, name ='patient_list_view'),
    path('patients/<int:pk>/', patient_detail_view, name='patient_detail_view'),
    path('patients/create/', create_update_patient_view, name='create_patient_view'),
    path('patients/update/<int:pk>/', create_update_patient_view, name='update_patient_view'),
    path('patients/delete/<int:pk>/', delete_patient_view, name='delete_patient_view'),

]

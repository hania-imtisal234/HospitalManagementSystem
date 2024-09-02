from django.contrib import admin
from .models import DoctorProfile
# Register your models here.

class DoctorProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)  
    list_display = ('full_name', 'email', 'specialization', 'created_at')
    search_fields = ('full_name', 'email', 'specialization')
    list_filter = ('specialization',)
    ordering = ('full_name',)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.user = request.user 
             
        super().save_model(request, obj, form, change)
        
admin.site.register(DoctorProfile,DoctorProfileAdmin)

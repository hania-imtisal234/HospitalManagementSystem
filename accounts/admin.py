from django.contrib import admin
from .models import CustomUser  # Import the CustomUser model

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'role', 'specialization', 'created_at')
    search_fields = ('full_name', 'email', 'role', 'specialization')
    list_filter = ('role', 'specialization', 'gender')
    ordering = ('full_name',)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  
            obj.user = request.user  # Set the user as the current logged-in admin
            
        super().save_model(request, obj, form, change)

# Register the CustomUser model with the admin site using the CustomUserAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)

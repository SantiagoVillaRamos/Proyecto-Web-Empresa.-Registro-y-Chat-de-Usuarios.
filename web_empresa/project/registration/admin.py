from django.contrib import admin
from .models import Profile
# Register your models here.
# class ProfileAdmin(admin.ModelAdmin):
#     readonly_fields = ('user__username', )
    
admin.site.register(Profile)
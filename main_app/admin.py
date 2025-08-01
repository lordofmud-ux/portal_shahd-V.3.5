from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)
    

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email')

class AdminEmailModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin_email',)

    def admin_email(self, obj):
        return obj.admin.email if obj.admin else "-"
    admin_email.short_description = 'Email'
    def admin_first_name(self, obj):
        return obj.admin.first_name if obj.admin else "-"
    admin_first_name.short_description = 'First Name'

    def admin_last_name(self, obj):
        return obj.admin.last_name if obj.admin else "-"
    admin_last_name.short_description = 'Last Name'
    
admin.site.register(CustomUser, UserModel)
admin.site.register(Staff, AdminEmailModelAdmin)
admin.site.register(Sugar, AdminEmailModelAdmin) 
admin.site.register(Kh, AdminEmailModelAdmin)
admin.site.register(Person)
admin.site.register(Holding, AdminEmailModelAdmin)
admin.site.register(Piran, AdminEmailModelAdmin)
admin.site.register(Tomato, AdminEmailModelAdmin)  
admin.site.register(Taraghi, AdminEmailModelAdmin)
admin.site.register(Tootia, AdminEmailModelAdmin)
admin.site.register(Drug, AdminEmailModelAdmin)
admin.site.register(Gen, AdminEmailModelAdmin)
admin.site.register(Iron, AdminEmailModelAdmin)
admin.site.register(Ptro, AdminEmailModelAdmin)
admin.site.register(Agriculture, AdminEmailModelAdmin)
admin.site.register(Research, AdminEmailModelAdmin)
admin.site.register(Organ)
admin.site.register(Subject)
admin.site.register(Session)


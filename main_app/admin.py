from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Sugar)
admin.site.register(Kh)
admin.site.register(Person)
admin.site.register(Holding)
admin.site.register(Piran)
admin.site.register(Tomato)
admin.site.register(Taraghi)
admin.site.register(Tootia)
admin.site.register(Drug)
admin.site.register(Gen)
admin.site.register(Iron)
admin.site.register(Ptro)
admin.site.register(Agriculture)
admin.site.register(Research)
admin.site.register(Organ)
admin.site.register(Subject)
admin.site.register(Session)

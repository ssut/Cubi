from django.contrib import admin
from member.models import CubiUser

class CubiUserAdmin(admin.ModelAdmin):
    list_display = ['type', 'username', 'nickname']

admin.site.register(CubiUser, CubiUserAdmin)
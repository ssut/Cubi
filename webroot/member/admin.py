from django.contrib import admin
from member.models import TinicubeUser

class TinicubeUserAdmin(admin.ModelAdmin):
    list_display = ['type', 'username', 'nickname']

admin.site.register(TinicubeUser, TinicubeUserAdmin)
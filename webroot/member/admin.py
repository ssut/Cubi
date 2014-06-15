from django.contrib import admin
from member.models import TinicubeUser, UserAuthorFavorites, UserWorkFavorites

class TinicubeUserAdmin(admin.ModelAdmin):
    list_display = ['type', 'username', 'nickname']

admin.site.register(TinicubeUser, TinicubeUserAdmin)
admin.site.register(UserAuthorFavorites)
admin.site.register(UserWorkFavorites)
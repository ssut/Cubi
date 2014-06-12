from django.contrib import admin
from work.models import *

class WorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'created']

class WorkCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'work', 'content', 'created']

class ChapterAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'work', 'created']

class ContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'sequence', 'chapter']

admin.site.register(Work, WorkAdmin)
admin.site.register(WorkComment, WorkCommentAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(ChapterRating)
admin.site.register(Image)
admin.site.register(Content, ContentAdmin)

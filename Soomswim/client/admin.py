from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'profile']
    list_display_links = ['name', 'profile']
    list_per_page = 20

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'writer', 'date', 'text']
    list_display_links = ['writer', 'date', 'text']
    list_per_page = 20

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'writer', 'caller', 'date', 'text', 'story']
    list_display_links = ['writer', 'caller', 'date', 'text', 'story']
    list_per_page = 20

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ['id', 'requester', 'receiver', 'state']
    list_display_links = ['requester', 'receiver', 'state']
    list_per_page = 20


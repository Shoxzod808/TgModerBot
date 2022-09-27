from django.contrib import admin
from .models import BotUser, Template

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'chat_id', 'username', 'language', 'created']

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'body_ru', 'body_eng']
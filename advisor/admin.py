from django.contrib import admin

# Register your models here.

from advisor.models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    search_fields = ('user__username', 'text')
    list_filter = ('role', 'created_at')

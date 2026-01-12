from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'role', 'short_content')
    list_filter = ('role', 'created_at')
    search_fields = ('content', 'user__username')

    def short_content(self, obj):
        return obj.content[:80]

    short_content.short_description = 'content'

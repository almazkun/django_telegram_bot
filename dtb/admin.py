from django.contrib import admin
from django.contrib.auth import get_user_model

from dtb.models import Bot, BotCommand, Chat, Message


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_staff", "is_superuser")
    search_fields = ("username",)


class BotAdmin(admin.ModelAdmin):
    list_display = ("name", "auth_token", "created_at")
    search_fields = ("name", "auth_token")
    fields = ("name", "uuid", "auth_token", "secret_token", "created_at", "created_by")
    readonly_fields = ("uuid", "auth_token", "secret_token", "created_at", "created_by")


class ChatAdmin(admin.ModelAdmin):
    list_display = ("chat_id", "bot", "chat_info", "created_at")
    search_fields = ("chat_id",)
    fields = ("chat_id", "bot", "chat_info", "created_at")
    readonly_fields = ("chat_id", "bot", "chat_info", "created_at")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("chat", "sender", "text_short")
    search_fields = ("chat", "text")
    fields = ("chat", "text", "from_user", "message_info", "created_at")
    readonly_fields = ("chat", "text", "from_user", "message_info", "created_at")

    def text_short(self, obj):
        return str(obj)


class BotCommandAdmin(admin.ModelAdmin):
    list_display = ("command", "bot")
    search_fields = ("command", "bot")
    fields = ("command", "response", "bot", "created_at")
    readonly_fields = ("created_at",)


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Bot, BotAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(BotCommand, BotCommandAdmin)

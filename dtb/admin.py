from django.contrib import admin
from dtb.models import TelegramBot


class TelegramBotAdmin(admin.ModelAdmin):
    pass


admin.site.register(TelegramBot, TelegramBotAdmin)

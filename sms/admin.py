from django.contrib import admin
from .models import SendingMessages, Client, Message


admin.site.register(SendingMessages)
admin.site.register(Client)
admin.site.register(Message)

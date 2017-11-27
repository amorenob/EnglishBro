from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Audio)
admin.site.register(AudioChunk)
admin.site.register(Transcript)
admin.site.register(UserConnection)
admin.site.register(Conversation)
admin.site.register(Message)
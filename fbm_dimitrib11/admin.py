from django.contrib import admin
from .models import Audio, AudioChunk, Transcript, User
# Register your models here.
admin.site.register(User)
admin.site.register(Audio)
admin.site.register(AudioChunk)
admin.site.register(Transcript)
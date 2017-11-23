from django.contrib import admin
from .models import Audio, AudioChunk, Transcript
# Register your models here.
admin.site.register(Audio)
admin.site.register(AudioChunk)
admin.site.register(Transcript)
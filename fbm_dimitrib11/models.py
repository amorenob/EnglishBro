from django.db import models

# Create your models here.
class Audio(models.Model):
	name = models.CharField(max_length=200)

class AudioChunk(models.Model):
	#Sequense id
	audio_id = models.ForeignKey(Audio, on_delete = models.CASCADE) 
	seq_id = models.IntegerField()
	url_link = models.CharField(max_length=1000)
	def __str__(self):
		return self.audio_id.name + ' chunk #' + str(self.seq_id)

class Transcript(models.Model):
	chunk_id  = models.ForeignKey(AudioChunk, on_delete = models.CASCADE) 
	sender_psid = models.IntegerField()
	text = models.CharField(max_length=500)

	def __str__(self):
		return (str(self.sender_psid) + ' >> ' 
			+ self.chunk_id.audio_id.name + ' '
			+ 'chunk #' + str(self.chunk_id.seq_id) + ': ' 
			+ self.text)
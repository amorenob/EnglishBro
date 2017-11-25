from django.db import models

# Create your models here.

#Table to save user's details
class User(models.Model):
	#psid = models.IntegerField()
	first_name =  models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	profile_pic = models.CharField(max_length=500)
	locale =  models.CharField(max_length=20)
	timezone = models.IntegerField()
	gender = models.CharField(max_length=10)

	def __str__(self):
		return '{0} {1}, {2}'.format(
			self.first_name,
			self.last_name,
			self.locale)

# Table to save interaction of the user with the app
class UserConnection():
	pass

class Audio(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return '{0}'.format(
			self.name)

class AudioChunk(models.Model):
	#Sequense id
	audio = models.ForeignKey(Audio, on_delete = models.CASCADE) 
	seq_id = models.IntegerField()
	url_link = models.CharField(max_length=1000)
	def __str__(self):
		return '{0} chunk #{1}'.format(
			self.audio,
			str(self.seq_id)) 
		

class Transcript(models.Model):
	chunk = models.ForeignKey(AudioChunk, on_delete = models.CASCADE) 
	user = models.ForeignKey(User, on_delete = models.CASCADE) 
	text = models.CharField(max_length=500)

	def __str__(self):
		return '{0}, {1}: {2}'.format(
			self.user,
			self.chunk,
			self.text) 


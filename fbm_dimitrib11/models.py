from django.db import models
from django.utils import timezone


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
	level = models.PositiveIntegerField(default=0)

	def __str__(self):
		return '{0} {1}, {2}'.format(
			self.first_name,
			self.last_name,
			self.locale)

# Table to save interaction of the user with the app
class UserConnectionManager(models.Manager):
	def last_connection(self, user):
		return self.filter(user=user).count()
	def connection_count(self, user):
		return self.filter(user=user).count()

class UserConnection(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	date_time = models.DateTimeField(auto_now=True)
	duration = models.DurationField(null=True)
	'''
	definir manager para obtener ultima conexion
	
	'''
	def __str__(self):
		return '{0}, {1}, {2}'.format(
			self.user,
			self.date_time,
			self.duration)
	def update_duration(self):
		self.duration = (timezone.now() - self.date_time)
		self.save()


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
	length = models.IntegerField(default=0)
	level = models.PositiveIntegerField(default=0)

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

# save interaction with the bot
class Conversation(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	started_date_time = models.DateTimeField(default=timezone.now)
	finished_date_time = models.DateTimeField(default=timezone.now)
	active = models.BooleanField(default = True)

	def __str__(self):
		return '{0}, {1}: {2}'.format(
			self.user,
			self.id,
			self.active) 

# To save every activity with the bot 
class Message(models.Model):
	conversation = models.ForeignKey(Conversation, on_delete = models.CASCADE)
	type_of =  models.CharField(max_length=20)
	text = models.CharField(max_length=1000)

	def __str__(self):
		return '{0}: {1}'.format(
			self.conversation,
			self.text) 

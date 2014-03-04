from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField

class Domain(models.Model):
	slug = models.SlugField()
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Member(models.Model):
	domain = models.ForeignKey(Domain, default=None)
	user = models.OneToOneField(User)

	def __str__(self):
		return self.user.__str__()

class Skill(models.Model):
	member = models.ForeignKey(Member, default=None)
	category = models.CharField(max_length=200)
	description = models.TextField()

	def __str__(self):
		return self.category

class Offer(models.Model):
	STATE_CHOICES = (
		("new", "New"),
		("active", "Active"),
		("pending", "Pending"),
		("accepted", "Accepted"),
		("archived", "Archived"),
	)
	slug = AutoSlugField(populate_from='title')
	title = models.CharField(max_length=20)
	member = models.ForeignKey(Member, default=None)
	state = models.CharField(max_length=20, choices=STATE_CHOICES)
	organization = models.CharField(max_length=300)
	date_posted = models.DateTimeField(auto_now_add=True)
	date_last_modified = models.DateTimeField(auto_now=True)
	description = models.TextField()
	contact_email = models.EmailField()

	def __str__(self):
		return self.title
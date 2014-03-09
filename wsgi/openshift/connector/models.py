from django.db import models
from django.core.urlresolvers import reverse
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

	def get_absolute_url(self):
		return reverse('profile_url', args=[self.id])

class Skill(models.Model):
	member = models.ForeignKey(Member, default=None)
	category = models.CharField(max_length=200)
	description = models.TextField()

	def __str__(self):
		return self.category

class Offer(models.Model):
	STATE_NEW = 0
	STATE_ACTIVE = 1
	STATE_PENDING = 2
	STATE_ACCEPTED = 3
	STATE_ARCHIVED = 4

	STATE_CHOICES = (
		(STATE_NEW, "New"),
		(STATE_ACTIVE, "Active"),
		(STATE_PENDING, "Pending"),
		(STATE_ACCEPTED, "Accepted"),
		(STATE_ARCHIVED, "Archived"),
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
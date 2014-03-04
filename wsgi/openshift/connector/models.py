from django.db import models

class Domain(models.Model):
	name = models.CharField(max_length=200)

class Member(models.Model):
	domain = models.ForeignKey(Domain, default=None)

class Skill(models.Model):
	member = models.ForeignKey(Member, default=None)
	category = models.CharField(max_length=200)
	description = models.TextField()

class Offer(models.Model):
	STATE_CHIOICES = (
		("new", "New"),
		("active", "Active"),
		("pending", "Pending"),
		("accepted", "Accepted"),
		("archived", "Archived"),
	)
	state = models.CharField(max_length=20, choices=STATE_CHIOICES)
	organization = models.CharField(max_length=300)
	date_posted = models.DateTimeField(auto_now_add=True)
	date_last_modified = models.DateTimeField(auto_now=True)
	description = models.TextField()
	contact_email = models.EmailField()
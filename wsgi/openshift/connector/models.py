from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from autoslug import AutoSlugField

import os

class Domain(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Member(models.Model):
    MODE_FREELANCER = 0
    MODE_POSTER = 1

    MODE_CHOICES = (
        (MODE_FREELANCER, "Freelancer"),
        (MODE_POSTER, "Poster")
    )
    domain = models.ForeignKey(Domain, default=None)
    user = models.OneToOneField(User)
    is_setup = models.BooleanField(editable=False, default=False)
    mode = models.IntegerField(editable=True, choices=MODE_CHOICES, default=MODE_FREELANCER)

    def __str__(self):
        return self.user.__str__()

    def is_poster(self):
        return self.mode == MODE_POSTER

    def is_freelancer(self):
        return self.mode == MODE_FREELANCER
     
    def get_absolute_url(self):
        return reverse('profile_url', args=[self.id])

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", blank=True, null=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    member = models.ForeignKey(Member, default=None)
    category = models.ForeignKey(Category, default=None)
    description = models.TextField()

    class Meta:
        unique_together = (("member", "category"),)

    def __str__(self):
        return self.category.__str__()

    def get_absolute_url(self):
        return reverse('skill_detail_url', args=[self.id])

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
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category)
    member = models.ForeignKey(Member, default=None)
    state = models.IntegerField(max_length=20, choices=STATE_CHOICES)
    organization = models.CharField(max_length=300)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField()
    contact_email = models.EmailField()
    bid_low = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bid_high = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def is_free(self):
        return self.bid_high == self.bid_low and self.bid_low == 0

    def is_set_bid(self):
        return self.bid_low == self.bid_high

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('offer_detail_url', args=[self.id])

    def format_bid_string(self):
        if self.is_free():
            return "Free"
        elif offer.is_set_bid():
            return "$"+ intcomma(floatformat(self.bid_low, 2))
        else:
            return "P"

from django.db import models
from django.forms import ModelForm
from models import *

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'organization', 'contact_email']

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'description']
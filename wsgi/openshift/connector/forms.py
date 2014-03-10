from django.db import models
from django.forms import ModelForm
from connector.models import *

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'organization', 'contact_email', 'bid_low', 'bid_high']

        labels = {
            'bid_low': 'Minimum Bid',
            'bid_high': 'Maximum Bid',
        }
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'description']

from django.db import models
from django.forms import ModelForm, Form, CharField
from django.forms.models import inlineformset_factory
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

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['domain', 'avatar']

class SignupForm(Form):
    #first_name = CharField(max_length=30, label='First Name')
    #last_name = CharField(max_length=30, label='Last Name')

    def save(self, user):
        #user.first_name = self.cleaned_data['first_name']
        #user.last_name = self.cleaned_data['last_name']
        user.save()

    def signup(self, request, user):
        member = Member()
        member.user = user
        member.domain = Domain.objects.all()[0]
        member.save()
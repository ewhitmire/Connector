from django.db import models
from django.forms import ModelForm, Form, CharField
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from connector.models import *
import autocomplete_light
from haystack.forms import FacetedSearchForm

class OfferForm(autocomplete_light.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'description', 'organization', 'contact_email', 'bid_low', 'bid_high', 'category', 'tags']

        labels = {
            'bid_low': 'Minimum Bid',
            'bid_high': 'Maximum Bid',
        }

class SkillForm(autocomplete_light.ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'description', 'tags']

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove('member') # allow checking against the missing attribute

        try:
            self.instance.validate_unique(exclude=exclude)
        except ValidationError as e:
            self._update_errors(e)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['domain', 'about']

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

class DrillDownSearchForm(FacetedSearchForm):
    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset.all()

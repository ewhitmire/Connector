from django.db import models
from django.forms import ModelForm, Form, CharField, BooleanField
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from connector.models import *
import autocomplete_light
from haystack.forms import FacetedSearchForm

class OfferForm(autocomplete_light.ModelForm):
    required_css_class = 'required'
    independent = BooleanField(required=False)
    class Meta:
        model = Offer
        fields = ['title', 'category', 'description', 'organization', 'contact_email', 'cost', 'negotiable', 'cost_notes', 'time', 'tags']

        labels = {
            'cost': 'Budget',
            'cost_notes': 'Notes',
            'time': 'Expected Time Commitment',
        }

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        field_order = self.fields.keyOrder
        field_order.pop(field_order.index('independent'))
        field_order.insert(4, 'independent')

    def clean(self):
        cleaned_data = super(OfferForm, self).clean()
        organization = cleaned_data.get("organization")
        independent = cleaned_data.get("independent")

        if (not independent) and len(organization)==0:
            raise ValidationError("Enter an organization or check Independent")
        return cleaned_data

class SkillForm(autocomplete_light.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Skill
        fields = ['category', 'description', 'experience', 'portfolio', 'tags']

        labels = {
            'experience': 'Duration of experience in this area',
            'portfolio': 'Link to online portfolio',
        }
    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove('member') # allow checking against the missing attribute

        try:
            self.instance.validate_unique(exclude=exclude)
        except ValidationError as e:
            self._update_errors(e)

class UserForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class MemberForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Member
        fields = ['domain', 'about']

class SignupForm(Form):
    required_css_class = 'required'
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
    required_css_class = 'required'
    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset.all()

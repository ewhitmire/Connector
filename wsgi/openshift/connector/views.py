from django.shortcuts import render

from django.views.generic import *
from connector.models import *
from connector.forms import *

# Create your views here.
class ProfileView(DetailView):
    model = Member
    template_name = 'members/profile.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        return context

class OffersView(ListView):
    model = Offer
    template_name = 'offers/offers.html'
    context_object_name = 'offers'

    def get_context_data(self, **kwargs):
        context = super(OffersView, self).get_context_data(**kwargs)

        return context


class CreateOfferView(CreateView):
    model = Offer
    object = model
    form_class = OfferForm
    template_name = 'offers/create.html'

    def get_context_data(self, **kwargs):
        return kwargs


    def post(self, request, *args, **kwargs):
        form = OfferForm(request.POST)

        if form.is_valid():
            offer = form.save()

            return HttpResponseRedirect(reverse('connector:offers_url'))
        else:
            return self.render_to_response(self.get_context_data(form=form))


class SkillsView(ListView):
    model = Skill
    template_name = 'skills/skills.html'
    context_object_name = 'skills'

    def get_context_data(self, **kwargs):
        context = super(SkillsView, self).get_context_data(**kwargs)

        return context


class CreateSkillsView(CreateView):
    model = Skill
    object = model
    form_class = SkillForm
    template_name = 'skills/create.html'

    def get_context_data(self, **kwargs):
        return kwargs


    def post(self, request, *args, **kwargs):
        form = SkillForm(request.POST)

        if form.is_valid():
            skill = form.save()

            return HttpResponseRedirect(reverse('connector:skills_url'))
        else:
            return self.render_to_response(self.get_context_data(form=form))
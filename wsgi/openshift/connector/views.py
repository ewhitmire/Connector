from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import *
from connector.models import *
from connector.forms import *

class ProfileView(DetailView):
    model = Member
    template_name = 'members/profile.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        return context

class MyProfileView(ProfileView):
    def get_object(self):
        return self.request.user

class OffersView(ListView):
    model = Offer
    template_name = 'offers/offers.html'
    context_object_name = 'offers'
    paginate_by = 10

    def get_queryset(self):
        cat_pk = self.kwargs.get('pk', None)
        if cat_pk is None:
            return Offer.objects.all()

        category = get_object_or_404(Category, pk=cat_pk)
        return Offer.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super(OffersView, self).get_context_data(**kwargs)
        cat_pk = self.kwargs.get('pk', None)
        if not cat_pk is None:
            category = get_object_or_404(Category, pk=cat_pk)
            context["category"] = category

        return context
class CreateOfferView(CreateView):
    model = Offer
    object = model
    form_class = OfferForm
    template_name = 'offers/create.html'

    def get_context_data(self, **kwargs):
        return kwargs


    def post(self, request, *args, **kwargs):
        member = request.user.member

        if request.method == 'POST':
            form = OfferForm(request.POST)

            if form.is_valid():
                self.object = form.save(commit=False)
                self.object.member = member
                self.object.save()

                return HttpResponseRedirect(reverse('offers_url'))
            else:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            form = OfferForm()

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
        member = request.user.member
        if request.method == 'POST':
            form = SkillForm(request.POST)

            if form.is_valid():
                self.object = form.save(commit=False)
                self.object.member = member
                self.object.save()

                return HttpResponseRedirect(reverse('skills_url'))
            else:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            form = SkillForm()
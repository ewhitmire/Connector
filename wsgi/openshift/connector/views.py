from django.core.urlresolvers import reverse, reverse_lazy
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

class MemberUpdateView(DetailView):
    model = Member
    template_name = 'members/member_update.html'

    def get_object(self):
        return self.request.user.member

    def get(self, request, *args, **kwargs):
        self.member_form = MemberForm(instance = request.user.member)
        self.user_form = UserForm(instance = request.user)
        return super(MemberUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.member_form = MemberForm(request.POST, request.FILES, instance = request.user.member)
        self.user_form = UserForm(request.POST, instance = request.user)
        if self.member_form.is_valid() and self.user_form.is_valid():
            self.user_form.save()
            member = self.member_form.save()
            member.is_setup = True
            member.save()
            return HttpResponseRedirect(reverse("my_profile_url"))
        else:
            return super(MemberUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberUpdateView, self).get_context_data(**kwargs)
        context['member_form'] = self.member_form
        context['user_form'] = self.user_form
        return context


class MyProfileView(ProfileView):

    def get_object(self):
        return self.request.user.member

    def get(self, request, *args, **kwargs):
        if not self.get_object().is_setup:
            return HttpResponseRedirect(reverse("member_update_url"))
        return super(MyProfileView, self).get(request, *args, **kwargs)

class OfferListView(ListView):
    model = Offer
    template_name = 'offers/offer_list.html'
    context_object_name = 'offers'
    paginate_by = 10

    def get_queryset(self):
        cat_pk = self.kwargs.get('pk', None)
        if cat_pk is None:
            return Offer.objects.all()

        category = get_object_or_404(Category, pk=cat_pk)
        return Offer.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super(OfferListView, self).get_context_data(**kwargs)
        cat_pk = self.kwargs.get('pk', None)
        if not cat_pk is None:
            category = get_object_or_404(Category, pk=cat_pk)
            context["category"] = category
        return context

class OfferCreateView(CreateView):
    model = Offer
    object = model
    form_class = OfferForm
    template_name = 'offers/offer_create.html'

    def post(self, request, *args, **kwargs):
        member = request.user.member

        if request.method == 'POST':
            form = OfferForm(request.POST)

            if form.is_valid():
                self.object = form.save(commit=False)
                self.object.member = member
                self.object.save()

                return HttpResponseRedirect(reverse('offer_list_url'))
            else:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            form = OfferForm()

class OfferDetailView(DetailView):
    model = Offer
    template_name = 'offers/offer_detail.html'

class OfferUpdateView(UpdateView):
    model = Offer
    form_class = OfferForm
    template_name = 'offers/offer_update.html'

class OfferDeleteView(DeleteView):
    model = Offer
    success_url = reverse_lazy('offer_list_url')
    template_name = 'offers/offer_confirm_delete.html'

class SkillListView(ListView):
    model = Skill
    template_name = 'skills/skill_list.html'
    context_object_name = 'skills'


class SkillCreateView(CreateView):
    model = Skill
    object = model
    form_class = SkillForm
    template_name = 'skills/skill_create.html'

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

                return HttpResponseRedirect(reverse('skill_list_url'))
            else:
                return self.render_to_response(self.get_context_data(form=form))
        else:
            form = SkillForm()

class SkillDetailView(DetailView):
    model = Skill
    template_name = 'skills/skill_detail.html'

class SkillUpdateView(UpdateView):
    model = Skill
    form_class = SkillForm
    template_name = 'skills/skill_update.html'

class SkillDeleteView(DeleteView):
    model = Skill
    success_url = reverse_lazy('skill_list_url')
    template_name = 'skills/skill_confirm_delete.html'

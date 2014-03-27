from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import *
from connector.models import *
from connector.forms import *
from connector.permissions import *
from haystack.views import *
from haystack.query import SearchQuerySet

class HomeView(TemplateView):
    template_name = 'home/index.html'

class CreateMemberFreelancerView(View):
    def get(self, request):
        request.session['signup_mode'] = Member.MODE_FREELANCER
        return redirect('account_signup')

class CreateMemberPosterView(View):
    def get(self, request):
        request.session['signup_mode'] = Member.MODE_POSTER
        return redirect('account_signup')


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
            member.mode = request.session.pop('signup_mode')
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


class OfferRelatedListView(ListView):
    model = Offer
    template_name = 'offers/offer_list.html'
    context_object_name = 'offers'

    def get_queryset(self):
        my_skills = Skill.objects.filter(member=self.request.user.member)
        categories = my_skills.values_list('category', flat=True)
        return Offer.objects.filter(category__in=categories).exclude(member=self.request.user.member)

class OfferRelatedView(ListView):
    model = Offer
    template_name = 'offers/offer_list.html'
    context_object_name = 'offers'

    def get_queryset(self):
        skill = get_object_or_404(Skill, pk=self.kwargs.get('pk', None))
        return Offer.objects.filter(category=skill.category).exclude(member=self.request.user.member)

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
                self.object.state = Offer.STATE_ACTIVE
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

    def dispatch(self, request, *args, **kwargs):
        offer = get_object_or_404(Offer, pk=kwargs.get('pk', None))

        if can_user_edit_offer(request.user, offer):
            return super(OfferUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You do not have permission to edit this offer.')

class OfferDeleteView(DeleteView):
    model = Offer
    success_url = reverse_lazy('offer_list_url')
    template_name = 'offers/offer_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        offer = get_object_or_404(Offer, pk=kwargs.get('pk', None))

        if can_user_edit_offer(request.user, offer):
            return super(OfferDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You do not have permission to delete this offer.')

class SkillRelatedListView(ListView):
    model = Skill
    template_name = 'skills/skill_list.html'
    context_object_name = 'skills'

    def get_queryset(self):
        my_offers = Offer.objects.filter(member=self.request.user.member)
        categories = my_offers.values_list('category', flat=True)
        return Skill.objects.filter(category__in=categories).exclude(member=self.request.user.member)

class SkillRelatedView(ListView):
    model = Skill
    template_name = 'skills/skill_list.html'
    context_object_name = 'skills'

    def get_queryset(self):
        offer = get_object_or_404(Offer, pk=self.kwargs.get('pk', None))
        return Skill.objects.filter(category=offer.category).exclude(member=self.request.user.member)

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
            s = Skill()
            s.category = Category.objects.all()[0]
            s.member = member
            form = SkillForm(request.POST, instance=s)
            if form.is_valid():
                
                self.object = form.save()

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

    def dispatch(self, request, *args, **kwargs):
        skill = get_object_or_404(Skill, pk=kwargs.get('pk', None))

        if can_user_edit_skill(request.user, skill):
            return super(SkillUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You do not have permission to update this skill.')

class SkillDeleteView(DeleteView):
    model = Skill
    success_url = reverse_lazy('skill_list_url')
    template_name = 'skills/skill_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        skill = get_object_or_404(Skill, pk=kwargs.get('pk', None))

        if can_user_edit_skill(request.user, skill):
            return super(SkillDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You do not have permission to delete this skill.')
from functools import update_wrapper
 
from django.conf import settings
from django.utils.decorators import classonlymethod
from django.views.generic.base import TemplateResponseMixin
 
from haystack.query import SearchQuerySet
from haystack.forms import FacetedSearchForm
from haystack.views import FacetedSearchView as HaystackFacetedSearchView
 
 

class FacetedSearchView(TemplateResponseMixin, HaystackFacetedSearchView):
    template_name = None
    facets = None
    filter_models = None
    order_by = None
    paginate_by = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)
    form_class = FacetedSearchForm
 
    def __init__(self, *args, **kwargs):
        form_class = kwargs.get('form_class', self.form_class)
        super(FacetedSearchView, self).__init__(*args, **kwargs)
        # Needed to switch out the default form class.
        self.form_class = form_class
        if not self.results_per_page and self.paginate_by:
            self.results_per_page = self.paginate_by
 
    def get_context_data(self):
        return {}
 
    def extra_context(self):
        ctx = super(FacetedSearchView, self).extra_context()
        ctx.update(self.get_context_data())
        return ctx
 
    def get_facets(self):
        if not self.facets:
            return []
        return self.facets
 
    def get_filter_model(self, models=None):
        if models:
            return (models + self.filter_models)
        return self.filter_models
 
    def get_order_by_fields(self):
        return self.order_by
 
    def get_extra_filters(self):
        return {}
 
    def get_search_queryset(self, queryset=None, models=None):
        searchqueryset = queryset or self.searchqueryset or SearchQuerySet()
        searchqueryset = searchqueryset.filter(
            **self.get_extra_filters()
        )
        for facet_field in self.get_facets():
            searchqueryset = searchqueryset.facet(facet_field)
        # check we should filter by model
        filter_models = self.get_filter_model(models)
        if filter_models:
            searchqueryset = searchqueryset.models(*filter_models)
        # check for defined order by list
        if self.get_order_by_fields():
            searchqueryset = searchqueryset.order_by(
                *self.get_order_by_fields()
            )
        return searchqueryset
 
    @property
    def template(self):
        """ Provide property to be backwards compatible with haystack. """
        template_names = self.get_template_names()
        if template_names:
            return template_names[0]
        return None
 
    def get(self, request, *args, **kwargs):
        self.searchqueryset = self.get_search_queryset()
        return super(FacetedSearchView, self).__call__(request)
 
    def __call__(self, request, *args, **kwargs):
        self.request = request
        self.kwargs = kwargs
        return self.get(request, *args, **kwargs)
 
    @classonlymethod
    def as_view(cls, *initargs, **initkwargs):
        def view(request, *args, **kwargs):
            return cls(*initargs, **initkwargs)(request, *args, **kwargs)
        update_wrapper(view, cls, updated=())
        return view

class SkillListView(FacetedSearchView):

    template='skills/skill_list.html'
    form_class=DrillDownSearchForm

    def build_form(self, form_kwargs=None):
        self.searchqueryset = SearchQuerySet().models(Skill).facet('category')
        return super(SkillListView, self).build_form(form_kwargs)

class SkillMemberView(FacetedSearchView):

    template='skills/skill_list.html'
    form_class = DrillDownSearchForm

    def build_form(self, form_kwargs=None):
        self.searchqueryset = SearchQuerySet().models(Skill).filter(member=Member.objects.get(pk=self.kwargs.get("mem_pk", None)))
        return super(SkillMemberView, self).build_form(form_kwargs)

class OfferListView(FacetedSearchView):

    template='offers/offer_list.html'
    form_class=DrillDownSearchForm

    def build_form(self, form_kwargs=None):
        self.searchqueryset = SearchQuerySet().models(Offer).facet('category')
        return super(OfferListView, self).build_form(form_kwargs)

class OfferMemberView(FacetedSearchView):

    template = 'offers/offer_list.html'
    form_class = DrillDownSearchForm

    def __call__(self, request, mem_pk):
        self.mem_pk = mem_pk
        return super(OfferMemberView, self).__call__(request)

    def build_form(self, form_kwargs=None):
        #prop = Member.objects.get(pk=self.mem_pk).property
        self.searchqueryset = SearchQuerySet().models(Offer).filter(member=Member.objects.get(pk=self.mem_pk))

        return super(OfferMemberView, self).build_form(form_kwargs)

import autocomplete_light
# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()

from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin

from django.conf import settings

from haystack.forms import FacetedSearchForm
from connector.forms import DrillDownSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from connector.views import *

admin.autodiscover()

urlpatterns = patterns('haystack.views',
)

urlpatterns += patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home_url'),
    # url(r'^$', 'openshift.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^accounts/', include('allauth.urls')),
    (r'^avatar/', include('avatar.urls')),
    url(r'^people/signup/freelancer', CreateMemberFreelancerView.as_view(), name='create_member_freelancer_url'),
    url(r'^people/signup/poster', CreateMemberPosterView.as_view(), name='create_member_poster_url'),
    url(r'^people/(?P<pk>\d+)/$', login_required(ProfileView.as_view()), name='profile_url'),
    url(r'^people/me/$', login_required(MyProfileView.as_view()), name='my_profile_url'),
    url(r'^people/edit/$', login_required(MemberUpdateView.as_view()), name='member_update_url'),
    url(r'^skills/all$', SkillListView.as_view(), name='skill_list_url'),
    url(r'^skills/related$', SkillRelatedListView.as_view(), name='skill_related_list_url'),
    url(r'^skills/(?P<pk>\d+)/related$', OfferRelatedView.as_view(), name='offer_related_url'),
    #url(r'^skills/category/(?P<cat_pk>\d+)$', SkillListView.as_view(), name='skill_category_url'),
    url(r'^skills/member/(?P<mem_pk>\d+)$', SkillMemberView.as_view(), name='skill_member_url'),
    url(r'^skills/(?P<pk>\d+)$', SkillDetailView.as_view(), name='skill_detail_url'),
    url(r'^skills/(?P<pk>\d+)/update$', SkillUpdateView.as_view(), name='skill_update_url'),
    url(r'^skills/(?P<pk>\d+)/delete$', SkillDeleteView.as_view(), name='skill_delete_url'),
    url(r'^skills/new$', login_required(SkillCreateView.as_view()), name='skill_create_url'),
    url(r'^offers/all$', OfferListView.as_view(), name='offer_list_url'),
    url(r'^offers/related$', OfferRelatedListView.as_view(), name='offer_related_list_url'),
    url(r'^offers/(?P<pk>\d+)$', OfferDetailView.as_view(), name='offer_detail_url'),
    url(r'^offers/(?P<pk>\d+)/related$', SkillRelatedView.as_view(), name='skill_related_url'),
    #url(r'^offers/category/(?P<cat_pk>\d+)$', OfferListView.as_view(), name='offer_category_url'),
    url(r'^offers/member/(?P<mem_pk>\d+)$', OfferMemberView.as_view(), name='offer_member_url'),
    url(r'^offers/(?P<pk>\d+)/update$', OfferUpdateView.as_view(), name='offer_update_url'),
    url(r'^offers/(?P<pk>\d+)/delete$', OfferDeleteView.as_view(), name='offer_delete_url'),
    url(r'^offers/new$', login_required(OfferCreateView.as_view()), name='offer_create_url'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    url(r'^search/$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=SearchQuerySet().facet('category')), name='haystack_search'),
    #url(r'^search/', include('haystack.urls')),

)

urlpatterns+=patterns('django.contrib.auth.views',
    url(r'^login$','login',{'template_name':'login.html'}),)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}))
urlpatterns += staticfiles_urlpatterns()

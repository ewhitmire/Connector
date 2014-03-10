from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin

from django.conf import settings

from connector.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    # url(r'^$', 'openshift.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^people/(?P<pk>\d+)/$', login_required(ProfileView.as_view()), name='profile_url'),
    url(r'^people/me/$', login_required(MyProfileView.as_view()), name='my_profile_url'),
    url(r'^skills/all$', SkillsView.as_view(), name='skills_url'),
    url(r'^skills/new$', login_required(CreateSkillsView.as_view()), name='create_skill_url'),
    url(r'^offers/all$', OffersView.as_view(), name='offers_url'),
    url(r'^offers/category/(?P<pk>\d+)$', OffersView.as_view(), name='offers_category_url'),
    url(r'^offers/new$', login_required(CreateOfferView.as_view()), name='create_offer_url'),
    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns+=patterns('django.contrib.auth.views',
    url(r'^login$','login',{'template_name':'login.html'}),)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}))
urlpatterns += staticfiles_urlpatterns()

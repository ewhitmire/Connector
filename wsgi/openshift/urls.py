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
    url(r'^/people/(?P<pk>\w+)$', ProfileView.as_view(), name='profile_url'))

    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns+=patterns('django.contrib.auth.views',
    url(r'^login$','login',{'template_name':'login.html'}),)

urlpatterns += staticfiles_urlpatterns()

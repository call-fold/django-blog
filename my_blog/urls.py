from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'my_blog.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'article.views.home'),
                       url(r'^(?P<my_args>\d+)/$',
                           'article.views.detail', name='detail'),
                       url(r'^test/$', 'article.views.home'),
                       )

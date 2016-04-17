from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'my_blog.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'article.views.home', name='home'),
                       url(r'^(?P<id>\d+)/$',
                           'article.views.detail', name='detail'),
                       url(r'^archives/$', 'article.views.archives',
                           name='archives'),
                       url(r'^aboutme/$', 'article.views.about_me',
                           name='about_me'),
                       url(r'^tag(?P<tag>\w+)/$',
                           'article.views.search_tag', name='search_tag'),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.STATIC_PATH, 'show_indexes': True}),
                       url(r'^search/$', 'article.views.blog_search',
                           name='search'),
                       )
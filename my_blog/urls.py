from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from article.views import RSSFeed

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'my_blog.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', 'article.views.home', name='home'),
                       url(r'^archives/(?P<id>\d+)/$',
                           'article.views.detail', name='detail'),
                       url(r'^archives/$', 'article.views.archives',
                           name='archives'),
                       url(r'^aboutme/$', 'article.views.about_me',
                           name='about_me'),
                       url(r'^tag(?P<tag>\S+)/$',
                           'article.views.search_tag', name='search_tag'),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.STATIC_PATH, 'show_indexes': True}),
                       url(r'^search/$', 'article.views.blog_search',
                           name='search'),
                       # 新添加的urlconf, 并将name设置为RSS, 方便在模板中使用url
                       url(r'^feed/$', RSSFeed(), name="RSS"),
                       url(r'^sites/$', 'article.views.sites', name='sites'),
                       url(r'^google0ddbc93a09800a50.html/$', 'article.views.google_seo', name='google_seo'),
                       url(r'^laboratory/$', 'article.views.laboratory', name='laboratory'),
                       url(r'^movie_search/$', 'article.views.movie_search', name='movie_search'),
                       url(r'^ajax_list/$', 'article.views.ajax_list', name='ajax-list'),
                       url(r'^movie_input_post/$', 'article.views.movie_input_post', name='movie_input_post'),
                       )

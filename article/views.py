from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse

from movie_crawler.movie_search import get_search_url, get_total_movie_download_list
from article.models import Article
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.syndication.views import Feed

# Create your views here.

# global
input_movie_name = ''


def home(request):
    posts = Article.objects.all()  # 获取全部的Article对象
    paginator = Paginator(posts, 2)  # 每页显示两个
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list})


def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post})


def archives(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'post_list': post_list,
                                             'error': False})


def about_me(request):
    return render(request, 'aboutme.html')


def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact=tag)  # contains
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'tag.html', {'post_list': post_list})


# def movie_search(request):
#     ctx = {}
#     ctx.update(csrf(request))
#     if request.POST:
#         input_name = request.POST['m']
#         my_search_index_url = get_search_url('http://s.dydytt.net/plus/search.php?kwtype=0&searchtype=title&keyword=',
#                                              input_name)
#         search_movie_download_list = get_total_movie_download_list(my_search_index_url, 'gbk', False)
#
#         out_str = ''
#         if len(search_movie_download_list) != 0:
#             for download_link in search_movie_download_list:
#                 out_str += download_link + '\n' + '\n'
#         else:
#             out_str += '没有找到合适的资源'
#
#         ctx['rlt'] = out_str
#
#     return render(request, "movie_search.html", ctx)


def movie_input_post(request):
    if request.is_ajax():
        if request.POST:
            global input_movie_name
            input_movie_name = request.POST['input_movie_name']
        message = "Yes, AJAX!"
    else:
        message = "Not Ajax"
    return HttpResponse(message)


def ajax_list(request):
    input_name = input_movie_name
    my_search_index_url = get_search_url('http://s.dydytt.net/plus/search.php?kwtype=0&searchtype=title&keyword=',
                                         input_name)
    search_movie_download_list = get_total_movie_download_list(my_search_index_url, 'gbk', False)
    out_list = []
    if len(search_movie_download_list) != 0:
        for download_link in search_movie_download_list:
            out_list.append(download_link)
            out_list.append('\n')
            out_list.append('\n')
    else:
        out_list.append('没有找到合适的资源, 我也很无奈啊...╮(╯﹏╰)╭')

    return JsonResponse(out_list, safe=False)


def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request, 'home.html')
        else:
            post_list = Article.objects.filter(title__icontains=s)
            if len(post_list) == 0:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': True})
            else:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': False})
    return redirect('/')


class RSSFeed(Feed):
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content


def sites(request):
    return render(request, 'sites.html')


def laboratory(request):
    return render(request, 'laboratory.html')


def movie_search(request):
    return render(request, 'movie_search.html')


def google_seo(request):
    return render(request, 'google0ddbc93a09800a50.html')

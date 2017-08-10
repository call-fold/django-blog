from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse

from movie_crawler.movie_search_from_redis import get_movie_db_list
from movie_crawler.movie_search import get_search_url, get_total_movie_download_list, get_dytt_search_url, \
    get_none_resources_context
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


def movie_input_post(request):
    if request.is_ajax():
        if request.POST:
            global input_movie_name
            input_movie_name = request.POST['input_movie_name']
        message = "Yes, AJAX!"
    else:
        message = "Not Ajax"
    return HttpResponse(message)


def union_two_list(list_db, list_search):
    set_db = set(list_db)
    set_search = set(list_search)
    set_db.update(set_search)
    return set_db


def search_from_web(dytt_search_url, input_name):
    out_list = []
    my_search_index_url = get_search_url(dytt_search_url,
                                         input_name)
    search_movie_download_list = get_total_movie_download_list(my_search_index_url, 'gbk', False)
    if len(search_movie_download_list) != 0:
        for download_link in search_movie_download_list:
            out_list.append(download_link)
    else:
        out_list.append(get_none_resources_context())
    return out_list


def structure_list(_total_link_list):
    _structure_total_list = []
    for link in _total_link_list:
        _structure_total_list.append(link)
        _structure_total_list.append('\n')
        _structure_total_list.append('\n')
    return _structure_total_list


def solve_repeated_list(_list):
    return list(set(_list))


def judge_search_result(_list):
    judge_list = _list
    if 0 == len(judge_list):
        judge_list.append('没有找到合适的资源, 我也很无奈啊...╮(╯﹏╰)╭')
    return judge_list


def ajax_list(request):
    input_name = input_movie_name
    movie_db_list = get_movie_db_list(input_name)
    db_list = []
    for db_link in movie_db_list:
        db_list.append(db_link)
    if 0 == len(db_list):
        search_list = search_from_web(get_dytt_search_url(), input_name)
        search_list = solve_repeated_list(search_list)
        structure_total_list = structure_list(search_list)
    else:
        db_list = solve_repeated_list(db_list)
        structure_total_list = structure_list(db_list)
    final_list = judge_search_result(structure_total_list)
    return JsonResponse(final_list, safe=False)


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


def movie_update(request):
    return render(request, 'movie_update.html')


def google_seo(request):
    return render(request, 'google0ddbc93a09800a50.html')

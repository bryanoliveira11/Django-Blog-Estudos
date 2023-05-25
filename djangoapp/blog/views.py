from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404

PER_PAGE = 9


def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'blog/pages/index.html', {
            'page_obj': page_obj,
            'title': 'Home |'
        }
        )


def post(request, slug):
    post_obj = Post.objects.get_published().filter(slug=slug).first()

    if post_obj is None:
        raise Http404()

    return render(
        request, 'blog/pages/post.html', {
            'post': post_obj,
            'title': f'{post_obj.title} |',
        }
        )


def page(request, slug):
    page_obj = Page.objects.get_published().filter(slug=slug).first()

    if page_obj is None:
        raise Http404()

    return render(
        request, 'blog/pages/page.html', {
            'page': page_obj,
            'title': f'{page_obj.title} |'
        }
        )


def created_by(request, author_pk):
    posts = Post.objects.get_published().filter(created_by__id=author_pk)
    user = User.objects.filter(pk=author_pk).first()
    user_full_name = user.username

    if user is None:
        raise Http404()

    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'blog/pages/index.html', {
            'page_obj': page_obj,
            'title': f'Posts de {user_full_name} |'
        }
        )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    return render(
        request, 'blog/pages/index.html', {
            'page_obj': page_obj,
            'title': f'{page_obj[0].category.name} |'
            }
        )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    return render(
        request, 'blog/pages/index.html', {
            'page_obj': page_obj,
            'title': f'{page_obj[0].tags.first().name} |'
        }
        )


def search(request):
    # search is the input field name
    search_value = request.GET.get('search').strip()

    posts = Post.objects.get_published().filter(
        Q(title__icontains=search_value) |
        Q(excerpt__icontains=search_value) |
        Q(content__icontains=search_value)
    )[0:PER_PAGE]

    return render(
        request, 'blog/pages/index.html', {
            'page_obj': posts,
            'search_value': search_value,
            'title': f'{search_value[:10]} - Search |'
        }
        )

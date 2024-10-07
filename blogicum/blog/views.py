from django.utils import timezone
from django.conf import settings

# Библиотеки сторонних разработчиков
from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Локальные импорты
from blog.models import Post, Category


def get_published_posts(now, category=None):
    if category:
        return Post.objects.filter(
            is_published=True,
            pub_date__lte=now,
            category=category
        )
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=now,
        category__is_published=True
    )


def index(request):
    now = timezone.now()
    post_list = get_published_posts(now)[:settings.POST_COUNT_ON_INDEX]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    now = timezone.now()
    post_list = get_published_posts(now)
    post = get_object_or_404(post_list, id=post_id)

    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if not category.is_published:
        raise Http404('Категория не опубликована.')

    now = timezone.now()
    post_list = get_published_posts(now, category)

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)

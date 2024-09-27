# Стандартные библиотеки
from django.utils import timezone
from django.conf import settings

# Библиотеки сторонних разработчиков
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Q


# Локальные импорты
from blog.models import Post, Category


def get_published_posts(now, category=None):
    if category:
        return Post.objects.filter(
            Q(is_published=True)
            & Q(pub_date__lte=now)
            & Q(category=category)
        )
    return Post.objects.filter(
        Q(is_published=True)
        & Q(pub_date__lte=now)
        & Q(category__is_published=True)
    )


def index(request):
    now = timezone.now()
    post_list = get_published_posts(now)[:settings.POST_COUNT_ON_INDEX]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    now = timezone.now()

    if (
        post.pub_date > now
        or not post.is_published
        or (post.category and not post.category.is_published)
    ):
        raise Http404("Пост не доступен")

    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if not category.is_published:
        raise Http404("Категория не опубликована.")

    now = timezone.now()
    post_list = get_published_posts(now, category)

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)

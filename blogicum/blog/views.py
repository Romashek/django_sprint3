from django.http import Http404
from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
from django.utils import timezone  # Используем timezone вместо datetime


def index(request):
    now = timezone.now()
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=now
    )[:5]
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
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=now  # Используем lte для включения текущего времени
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, get_object_or_404

# Локальные импорты
from blog.models import Post, Category


def get_published_posts():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )


def index(request):
    post_list = get_published_posts()[:settings.POST_COUNT_ON_INDEX]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post_list = get_published_posts()
    post = get_object_or_404(post_list, id=post_id)

    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = get_published_posts().filter(
        category=category
    )

    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)

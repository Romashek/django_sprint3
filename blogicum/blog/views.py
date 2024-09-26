from django.http import Http404
from django.shortcuts import render
from blog.models import Post, Category
from datetime import datetime


def index(request):
    post_list = Post.objects.all().filter(is_published=True,
                                          category__is_published=True,
                                          pub_date__lt=datetime.now())[:5]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except KeyError:
        raise Http404(f"Пост {post_id} не найден")
    if (
        post.pub_date > datetime.now()
        or not post.is_published
        or (post.category and not post.category.is_published)
    ):
        raise Http404("Пост не доступен")
    context = {'post': post, }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    if not category.is_published:
        raise Http404("Категория не опубликована.")
    post_list = Post.objects.all().filter(category=category,
                                          is_published=True,
                                          pub_date__lte=datetime.now())
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)

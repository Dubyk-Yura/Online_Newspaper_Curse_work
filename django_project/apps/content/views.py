from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from apps.subscriptions.models import UserSubscription
from core.singleton import SystemConfig
from .forms import PublicationForm, CommentForm, RatingForm
from .models import Publication, Category, Rating

User = get_user_model()


def articles_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    news_list = Publication.objects.filter(category=category).order_by('-created_at')

    return render(request, 'content/home.html', {
        'news_list': news_list,
        'page_title': f"Рубрика: {category.name}",  # Змінюємо заголовок сторінки
        'site_price': SystemConfig.get_instance().base_subscription_price,
    })


def home_page(request):
    all_news = Publication.objects.all().order_by('-created_at')

    paginator = Paginator(all_news, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    config = SystemConfig.get_instance()

    context = {
        'page_obj': page_obj,
        'news_list': page_obj,
        'site_price': config.base_subscription_price,
        'maintenance': config.maintenance_mode
    }

    return render(request, 'content/home.html', context)


def is_editor_check(user):
    return user.is_authenticated and (user.is_editor or user.is_superuser)


@login_required
@user_passes_test(is_editor_check)
def add_publication(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.author = request.user
            publication.save()

            messages.success(request, f"Новину '{publication.title}' успішно створено!")
            return redirect('home')
    else:
        form = PublicationForm()

    return render(request, 'content/publication_form.html', {
        'form': form,
        'title': 'Створити новину'
    })


@login_required
@user_passes_test(is_editor_check)
def edit_publication(request, pk):
    publication = get_object_or_404(Publication, pk=pk)

    if publication.author != request.user and not request.user.is_superuser:
        messages.error(request, "Ви не можете редагувати чужі новини.")
        return redirect('home')

    if request.method == 'POST':
        form = PublicationForm(request.POST, instance=publication)
        if form.is_valid():
            form.save()
            messages.success(request, "Зміни збережено!")
            return redirect('publication_detail', pk=publication.pk)
    else:
        form = PublicationForm(instance=publication)

    return render(request, 'content/publication_form.html', {
        'form': form,
        'title': 'Редагувати новину'
    })


def articles_by_author(request, author_id):
    author = get_object_or_404(User, pk=author_id)

    news_list = Publication.objects.filter(author=author).order_by('-created_at')

    return render(request, 'content/home.html', {
        'news_list': news_list,
        'page_title': f"Публікації автора: {author.username}",
        'is_author_feed': True
    })


def publication_detail(request, pk):
    post = get_object_or_404(Publication, pk=pk)

    has_access = False
    if not post.is_exclusive:
        has_access = True
    elif request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        has_access = True
    elif request.user.is_authenticated:
        try:
            sub = request.user.subscription
            if sub.check_access():
                has_access = True
        except UserSubscription.DoesNotExist:
            pass

    comments = post.comments.all()
    avg_rating = post.ratings.aggregate(Avg('value'))['value__avg'] or 0

    user_rating = None
    if request.user.is_authenticated:
        user_rating = post.ratings.filter(user=request.user).first()

    # Форми
    comment_form = CommentForm()
    rating_form = RatingForm()

    return render(request, 'content/detail.html', {
        'post': post,
        'has_access': has_access,
        'comments': comments,
        'avg_rating': round(avg_rating, 1),
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
    })


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Publication, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publication = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Коментар додано!')
    return redirect('publication_detail', pk=pk)


@login_required
def rate_publication(request, pk):
    post = get_object_or_404(Publication, pk=pk)
    if request.method == 'POST':
        if Rating.objects.filter(publication=post, user=request.user).exists():
            messages.warning(request, 'Ви вже оцінили цю статтю.')
        else:
            form = RatingForm(request.POST)
            if form.is_valid():
                rating = form.save(commit=False)
                rating.publication = post
                rating.user = request.user
                rating.save()
                messages.success(request, 'Дякуємо за вашу оцінку!')
    return redirect('publication_detail', pk=pk)


@login_required
def toggle_bookmark(request, pk):
    post = get_object_or_404(Publication, pk=pk)

    if post in request.user.bookmarks.all():
        request.user.bookmarks.remove(post)
        messages.info(request, "Статтю видалено із закладок.")
    else:
        request.user.bookmarks.add(post)
        messages.success(request, "Статтю додано в закладки!")

    return redirect(request.META.get('HTTP_REFERER', 'home'))

from .models import Publication
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from core.singleton import SystemConfig
from apps.subscriptions.models import UserSubscription
from .forms import PublicationForm
from django.contrib.auth import get_user_model

User = get_user_model()


def home_page(request):
    """
    Render main page with last news
    """
    news_list = Publication.objects.all().order_by('-created_at')  # get all news sorted by date

    config = SystemConfig.get_instance()

    context = {
        'news_list': news_list,
        'site_price': config.base_subscription_price,
        'maintenance': config.maintenance_mode
    }

    return render(request, 'content/home.html', context)


def is_editor_check(user):
    return user.is_authenticated and (user.is_editor or user.is_superuser)


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

    return render(request, 'content/detail.html', {
        'post': post,
        'has_access': has_access
    })


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

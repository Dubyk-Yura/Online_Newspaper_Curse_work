from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.subscriptions.models import UserSubscription
from apps.users.forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import User
from .forms import UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            UserSubscription.objects.create(user=user)

            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')


@login_required
def toggle_follow(request, author_id):
    author = get_object_or_404(User, id=author_id)

    if request.user == author:
        messages.warning(request, "Ви не можете підписатися на самого себе.")
        return redirect('home')

    if request.user.following.filter(id=author_id).exists():
        request.user.following.remove(author)
        messages.info(request, f"Ви відписалися від {author.username}.")
    else:
        request.user.following.add(author)
        messages.success(request, f"Ви підписалися на новини від {author.username}!")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профіль успішно оновлено!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    subscribed_authors = request.user.following.all()

    context = {
        'form': form,
        'subscribed_authors': subscribed_authors,
        'user': request.user
    }

    return render(request, 'users/profile.html', context)
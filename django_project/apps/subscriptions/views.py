from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, UserSubscription


def pricing_page(request):
    plans = SubscriptionPlan.objects.all().order_by('value')

    return render(request, 'subscriptions/pricing.html', {
        'plans': plans
    })


@login_required
def process_payment(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)

    subscription, created = UserSubscription.objects.get_or_create(user=request.user)

    subscription.plan = plan
    subscription.is_active = True

    subscription.expire_date = timezone.now().date() + timedelta(days=plan.duration_days)

    subscription.save()

    messages.success(request, f"Вітаємо! Ви підписалися на '{plan.name}'. Дійсна до: {subscription.expire_date}")
    return redirect('profile')
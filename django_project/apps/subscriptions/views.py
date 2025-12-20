from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubscriptionPlan, UserSubscription


def pricing_page(request):
    # Отримуємо всі плани, які мають ціну (або безкоштовні)
    plans = SubscriptionPlan.objects.all().order_by('value')

    return render(request, 'subscriptions/pricing.html', {
        'plans': plans
    })


@login_required
def process_payment(request, plan_id):
    """
    Імітація процесу оплати.
    В реальному житті тут був би редірект на Stripe/LiqPay.
    """
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)

    subscription, created = UserSubscription.objects.get_or_create(user=request.user)

    subscription.plan = plan
    subscription.is_active = True
    subscription.save()

    messages.success(request, f"Вітаємо! Ви успішно підписалися на план '{plan.name}'.")
    return redirect('home')
from django.db import migrations

def create_initial_plans(apps, schema_editor):
    SubscriptionPlan = apps.get_model('subscriptions', 'SubscriptionPlan')

    if not SubscriptionPlan.objects.filter(strategy_type='student').exists():
        SubscriptionPlan.objects.create(
            name='Student Plan',
            price_mode='percentage',
            value=50.00,
            duration_days=30,
            strategy_type='student'
        )

    if not SubscriptionPlan.objects.filter(strategy_type='corporate').exists():
        SubscriptionPlan.objects.create(
            name='Corporate Plan',
            price_mode='fixed',
            value=0.00,
            duration_days=365,
            strategy_type='corporate'
        )

    if not SubscriptionPlan.objects.filter(strategy_type='premium').exists():
        SubscriptionPlan.objects.create(
            name='Premium Plan',
            price_mode='percentage',
            value=100.00,
            duration_days=30,
            strategy_type='premium'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_initial_plans),
    ]
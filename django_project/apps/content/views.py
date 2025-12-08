from django.shortcuts import render
from .models import Publication
from core.singleton import SystemConfig

def home_page(request):
    """
    Render main page with last news
    """
    news_list = Publication.objects.all().order_by('-created_at') #get all news sorted by date

    config = SystemConfig.get_instance()

    context = {
        'news_list': news_list,
        'site_price': config.base_price,
        'maintenance': config.maintenance_mode
    }

    return render(request, 'content/home.html', context)
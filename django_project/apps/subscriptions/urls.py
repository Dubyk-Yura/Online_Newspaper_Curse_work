from django.urls import path
from . import views

urlpatterns = [
    path('', views.pricing_page, name='pricing'),
    path('buy/<int:plan_id>/', views.process_payment, name='subscribe'),
]
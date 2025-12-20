from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('publication/<int:pk>/', views.publication_detail, name='publication_detail'),
    path('publication/add/', views.add_publication, name='add_publication'),
    path('publication/<int:pk>/edit/', views.edit_publication, name='edit_publication'),
    path('author/<int:author_id>/', views.articles_by_author, name='articles_by_author'),
]

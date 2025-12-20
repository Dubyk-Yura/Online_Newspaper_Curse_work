from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('publication/<int:pk>/', views.publication_detail, name='publication_detail'),
    path('publication/add/', views.add_publication, name='add_publication'),
    path('publication/<int:pk>/edit/', views.edit_publication, name='edit_publication'),
    path('author/<int:author_id>/', views.articles_by_author, name='articles_by_author'),
    path('publication/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('publication/<int:pk>/rate/', views.rate_publication, name='rate_publication'),
    path('publication/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('category/<slug:slug>/', views.articles_by_category, name='articles_by_category'),
]

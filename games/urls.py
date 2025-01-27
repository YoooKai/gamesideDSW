from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game-list'),
    path('<slug:title>/', views.game_detail, name='game-detail'),
    path('<slug:title>/reviews/', views.review_list, name='review-list'),
    path('reviews/<pk>/', views.review_detail, name='review-detail'),
    path('<slug:title>/reviews/add/', views.add_review, name='add-review'),
]

from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game-list'),
    path('reviews/<pk>/', views.review_detail, name='review-detail'),
    path('<slug:slug>/reviews/', views.review_list, name='review-list'),
    path('<slug:slug>/', views.game_detail, name='game-detail'),
    path('<slug:slug>/reviews/add/', views.add_review, name='add-review'),
]

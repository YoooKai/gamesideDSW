from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<order_pk>/', views.order_detail, name='order-detail'),
    path('<order_pk>/games/', views.order_game_list, name='order-game-list'),
    path('<order_pk>/games/add/<slug:slug>/', views.add_game_to_order, name='add-game-to-order'),
    path('<order_pk>/games/status/', views.change_order_status, name='change-order-status'),
    path('<order_pk>/pay/', views.pay_order, name='pay-order'),
]

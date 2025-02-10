from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<pk>/', views.order_detail, name='order-detail'),
    path('<pk>/games/', views.order_game_list, name='order-game-list'),
    path('<pk>/games/add/<slug:slug>/', views.add_game_to_order, name='add-game-to-order'),
    path('<pk>/games/status/', views.change_order_status, name='change-order-status'),
    path('<pk>/pay/', views.pay_order, name='pay-order'),
]

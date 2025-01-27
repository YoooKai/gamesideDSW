from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<order_pk>/', views.order_detail, name='order-detail'),
    path('<order_pk>/games/', views.order_game_list, name='order-game-list'),
    path('<order_pk>/games/add/<slug:title>', views.add_game_to_order, name='add-game-to-order'),
    path('<order_pk>/confirm/', views.order_confirm, name='order_confirm'),
    path('<order_pk>/cancel/', views.order_cancel, name='order-cancel'),
    path('<order_pk>/pay/', views.pay_order, name='pay-order'),
]

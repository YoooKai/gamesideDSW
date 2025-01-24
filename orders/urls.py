from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<order_id>/', views.order_detail, name='order-detail'),
    path('<order_id>/confirm/', views.order_confirm, name='order_confirm'),
    path('<order_id>/cancel/', views.order_cancel, name='order-cancel'),
    path('<order_id>/pay/', views.pay_order, name='pay-order'),
]

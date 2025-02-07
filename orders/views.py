# Create your views here.
import json
import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from shared.decorators import check_method, token_checker
from users.models import Token

from .models import Order


@check_method('POST')
@token_checker
def add_order(request):
    PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
    token = request.headers.get('Authorization')
    clean_token = re.fullmatch(PATTERN, token)[1]
    print(clean_token)
    user = get_object_or_404(Token, key=clean_token).user
    order = Order.objects.create(
        user=user,
    )
    return JsonResponse({'id': order.pk}, status=200)


def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()
    pass


def order_game_list(request):
    pass


def add_game_to_order(request):
    pass


def change_order_status(request, pk):
    new_order_status = json.loads(request.body).get('status')
    order = Order.objects.filter(pk=pk)
    order.status = new_order_status
    return JsonResponse({'pk': order.pk}, status=200)


def pay_order(request):
    pass

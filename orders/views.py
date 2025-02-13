# Create your views here.
import json
import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from games.models import Game
from games.serializers import GameSerializer
from shared.decorators import (
    card_checker,
    check_method,
    field_checker,
    game_exists,
    json_checker,
    model_exists,
    owner_checker,
    token_checker,
)
from users.models import Token

from .models import Order
from .serializers import OrderSerializer


@check_method('POST')
@token_checker
def add_order(request):
    PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
    token = request.headers.get('Authorization')
    clean_token = re.fullmatch(PATTERN, token)['token']
    user = get_object_or_404(Token, key=clean_token).user
    order = Order.objects.create(
        user=user,
    )
    return JsonResponse({'id': order.pk}, status=200)


@check_method('GET')
@token_checker
@model_exists([Order, 'pk'])
@owner_checker
def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@check_method('GET')
@token_checker
@model_exists([Order, 'pk'])
@owner_checker
def order_game_list(request, pk):
    order = Order.objects.get(id=pk)
    serializer = GameSerializer(order.games.all(), request=request)
    return serializer.json_response()


@check_method('POST')
@json_checker
@field_checker(['game-slug'])
@token_checker
@model_exists([Order, 'pk'])
@game_exists
@owner_checker
def add_game_to_order(request, pk):
    slug = json.loads(request.body)['game-slug']
    game = Game.objects.get(slug=slug)
    if game.stock == 0:
        return JsonResponse({'error': 'Game out of stock'}, status=400)
    order = Order.objects.get(id=pk)
    order.games.add(game)
    order.save()
    game.stock -= 1
    game.save()
    return JsonResponse({'num-games-in-order': order.games.count()}, status=200)


@check_method('POST')
@json_checker
@field_checker(['status'])
@token_checker
@model_exists([Order, 'pk'])
@owner_checker
def change_order_status(request, pk):
    new_order_status = json.loads(request.body)['status']
    if new_order_status not in [Order.Status.CANCELLED, Order.Status.CONFIRMED]:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    order = Order.objects.get(pk=pk)
    if order.status != 1:
        return JsonResponse(
            {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
        )
    order.status = new_order_status
    for game in order.games.all():
        game.stock += 1

    order.save()
    return JsonResponse({'status': order.get_status_display()}, status=200)


@check_method('POST')
@json_checker
@field_checker(('card-number', 'exp-date', 'cvc'))
@token_checker
@model_exists([Order, 'pk'])
@owner_checker
@card_checker
def pay_order(request, pk):
    order = Order.objects.get(pk=pk)
    if order.status != Order.Status.CONFIRMED:
        return JsonResponse({'error': 'Orders can only be paid when confirmed'}, status=400)
    order.status = Order.Status.PAID
    order.save()
    return JsonResponse({'status': order.get_status_display()}, status=200)

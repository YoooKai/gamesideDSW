# Create your views here.
import json
import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from games.serializers import GameSerializer
from shared.decorators import check_method, existatata2, owner_checker, token_checker
from users.models import Token

from .models import Order
from .serializers import OrderSerializer
from games.models import Game


@check_method('POST')
@token_checker
def add_order(request):
    PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
    token = request.headers.get('Authorization')
    clean_token = re.fullmatch(PATTERN, token)[1]
    user = get_object_or_404(Token, key=clean_token).user
    order = Order.objects.create(
        user=user,
    )
    return JsonResponse({'id': order.pk}, status=200)


@check_method('GET')
@token_checker
@existatata2(Order)
@owner_checker
def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()

@check_method('GET')
@token_checker
@existatata2(Order)
@owner_checker
def order_game_list(request, pk):
    order = Order.objects.get(id=pk)
    serializer = GameSerializer(order.games.all(), request=request)
    return serializer.json_response()


def add_game_to_order(request ,slug):
    json_post = json.loads(request.body)
    PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
    token = request.headers.get('Authorization')
    clean_token = re.fullmatch(PATTERN, token)[1]
    game = get_object_or_404(Game, slug=slug)
    user = get_object_or_404(Token, key=clean_token).user
    review = Review.objects.create(
        
    )

    return JsonResponse({'id': review.pk}, status=200)


def change_order_status(request, pk):
    new_order_status = json.loads(request.body).get('status')
    order = Order.objects.filter(pk=pk)
    order.status = new_order_status
    return JsonResponse({'pk': order.pk}, status=200)


def pay_order(request):
    pass

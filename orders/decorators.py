import json
import re
from datetime import datetime
from django.http import JsonResponse
from games.models import Game
from orders.models import Order
from users.models import Token


def owner_checker(func):
    def wrapper(request, *args, **kwargs):
        PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
        token = request.headers.get('Authorization')
        clean_token = re.fullmatch(PATTERN, token)[1]
        order = Order.objects.get(pk=kwargs.get('pk'))
        user = Token.objects.get(key=clean_token)
        if user.user != order.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        return func(request, *args, **kwargs)

    return wrapper


def game_exists(func):
    def wrapper(request, *args, **kwargs):
        try:
            slug = json.loads(request.body).get('game-slug')
            Game.objects.get(slug=slug)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper


def card_checker(func):
    def wrapper(request, *args, **kwargs):
        card_number = json.loads(request.body)['card-number']
        exp_date = json.loads(request.body)['exp-date']
        cvc = json.loads(request.body)['cvc']
        if not re.fullmatch(r'^\d{4}-\d{4}-\d{4}-\d{4}$', card_number):
            return JsonResponse({'error': 'Invalid card number'}, status=400)
        
        if not re.fullmatch(r'^\d{2}/\d{4}$', exp_date):
            return JsonResponse({'error': 'Invalid expiration date'}, status=400)
        
        date_object = datetime.strptime(exp_date, '%m/%Y')
        if date_object < datetime.now():
            return JsonResponse({'error': 'Card expired'}, status=400)
        
        if not re.fullmatch(r'^\d{3}$', cvc):
            return JsonResponse({'error': 'Invalid CVC'}, status=400)

        return func(request, *args, **kwargs)

    return wrapper

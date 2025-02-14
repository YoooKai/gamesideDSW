import json
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .decorators import rating_checker

from shared.decorators import (
    check_method,
    field_checker,
    json_checker,
    model_exists,
    token_checker,
)
from users.models import Token

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


@check_method('GET')
@require_GET
def game_list(request):
    games = Game.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        games = games.filter(category__slug=category_slug)
    platform_slug = request.GET.get('platform')
    if platform_slug:
        games = games.filter(platforms__slug=platform_slug)
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@check_method('GET')
@model_exists([Game, 'game_slug'])
def game_detail(request, game_slug):
    games = Game.objects.get(slug=game_slug)
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@check_method('GET')
@model_exists([Game, 'game_slug'])
def review_list(request, game_slug):
    game = Game.objects.get(slug=game_slug)
    reviews = game.reviews.all()
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@check_method('GET')
@model_exists([Review, 'pk'])
def review_detail(request, pk):
    reviews = Review.objects.get(pk=pk)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@json_checker
@field_checker(('rating', 'comment'))
@rating_checker
@token_checker
@model_exists([Game, 'game_slug'])
@csrf_exempt
@require_POST
def add_review(request, game_slug):
    json_post = json.loads(request.body)
    PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
    token = request.headers.get('Authorization')
    clean_token = re.fullmatch(PATTERN, token)['token']
    game = Game.objects.get(slug=game_slug)
    user = Token.objects.get(key=clean_token).user
    review = Review.objects.create(
        **json_post,
        game=game,
        author=user,
    )

    return JsonResponse({'id': review.pk}, status=200)

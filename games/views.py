import json
import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from shared.decorators import (
    check_method,
    data_exists,
    field_checker,
    json_checker,
    model_check,
    rating_checker,
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
@data_exists(Game)
def game_detail(request, slug):
    games = Game.objects.get(slug=slug)
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@check_method('GET')
@data_exists(Game)
def review_list(request, slug):
    game = Game.objects.get(slug=slug)
    reviews = game.reviews.all()
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@check_method('GET')
@model_check(Review)
def review_detail(request, pk):
    reviews = Review.objects.get(pk=pk)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@json_checker
@field_checker(('rating', 'comment'))
@rating_checker
@token_checker
@data_exists(Game)
@csrf_exempt
@require_POST
def add_review(request, slug):
    json_post = json.loads(request.body)
    PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
    token = request.headers.get('Authorization')
    clean_token = re.fullmatch(PATTERN, token)[1]
    game = get_object_or_404(Game, slug=slug)
    user = get_object_or_404(Token, key=clean_token).user
    review = Review.objects.create(
        **json_post,
        game=game,
        author=user,
    )

    return JsonResponse({'id': review.pk}, status=200)

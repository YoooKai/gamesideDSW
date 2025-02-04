import json
import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from shared.decorators import check_method, existatata, token_checker
from users.models import Token

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


@check_method
@require_GET
def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@check_method
@existatata(Game)
def game_detail(request, slug):
    games = Game.objects.get(slug=slug)
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@check_method
def review_list(request, slug):
    game = Game.objects.get(slug=slug)
    reviews = game.reviews.all()
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@check_method
def review_detail(request, pk):
    reviews = Review.objects.get(pk=pk)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@token_checker
@csrf_exempt
@require_POST
def add_review(request, slug):
    json_post = json.loads(request.body)
    print(request.body)
    PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
    token = request.headers.get('Authorization')
    clean_token = re.fullmatch(PATTERN, token)[2]

    game = get_object_or_404(Game, slug=slug)
    user = get_object_or_404(Token, key=clean_token).user
    review = Review.objects.create(
        **json_post,
        game=game,
        author=user,
    )

    return JsonResponse({'id': review.pk}, status=200)

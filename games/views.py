import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from shared.decorators import check_method, existatata
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
    return serializer.json_response()  # no funciona


@check_method
def review_detail(request, pk):
    reviews = Review.objects.get(pk=pk)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()  # no funciona


@csrf_exempt
@require_POST
def add_review(request, slug):
    json_post = json.loads(request.body)
    game = get_object_or_404(Game, slug=slug)
    user = get_object_or_404(Token, user=request.user)
    review = Review.objects.create(
        rating=json_post['rating'],
        comment=json_post['comment'],
        game=game,
        author=user,
    )
    return JsonResponse({'id': review.pk})

    # comment = models.TextField()
    # rating = models.PositiveSmallIntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(5)]
    # )
    # game = models.ForeignKey('games.Game', related_name='reviews', on_delete=models.CASCADE)
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, related_name='author_reviews', on_delete=models.CASCADE
    # )
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

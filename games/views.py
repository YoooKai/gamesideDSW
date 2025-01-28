from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from shared.decorators import auth_required, check_method

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer


@check_method
@require_GET
def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@check_method
@require_GET
def game_detail(request, title):
    games = Game.objects.get(slug=title)
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@check_method
def review_detail(request, pk):
    reviews = Review.objects.get(pk=pk)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()  # no funciona


@check_method
def review_list(request, title):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()  # no funciona


@csrf_exempt
@require_POST
@auth_required
def add_review(request, game_slug):
    data = request.json
    game = get_object_or_404(Game, slug=game_slug)
    review = Review.objects.create(
        rating=data.get('rating'),
        comment=data.get('comment'),
        game=game,
        author=request.user,
    )
    return JsonResponse({'id': review.pk})

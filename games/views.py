from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from shared.decorators import auth_required

from .models import Game, Review
from .serializers import GameSerializer


@require_GET
def game_list(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


def game_detail(request, pk):
    pass


def review_detail(request, pk):
    pass


def review_list(request):
    pass


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

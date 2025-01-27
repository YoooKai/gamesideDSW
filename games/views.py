from .models import Game


def game_list(request):
    games = Game.objects.all()


def game_detail(request, pk):
    pass


def review_detail(request, pk):
    pass


def review_list(request):
    pass


def add_review(request):
    pass

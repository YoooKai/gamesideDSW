# Create your views here.
from serializers import OrderSerializer

from .models import Order


def add_order(request, slug):
    # data = request.json
    # game = get_object_or_404(Game, slug=slug)
    # order = Order.objects.create(
    #     rating=data.get('rating'),
    #     comment=data.get('comment'),
    #     game=game,
    #     author=request.user,
    # )
    # return JsonResponse({'id': review.pk})
    pass


def order_detail(request, pk):
    order = Order.objects.get(id=pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


def order_confirm(request):
    pass


def order_cancel(request):
    pass


def pay_order(request):
    pass


def order_game_list(request):
    pass


def add_game_to_order(request):
    pass

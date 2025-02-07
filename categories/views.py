from shared.decorators import check_method, existatata

from .models import Category
from .serializers import CategorySerializer


@check_method('GET')
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()


@check_method('GET')
@existatata(Category)
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()

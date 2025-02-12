from shared.decorators import check_method, data_exists

from .models import Category
from .serializers import CategorySerializer


@check_method('GET')
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()


@check_method('GET')
@data_exists(Category)
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()

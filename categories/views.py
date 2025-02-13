from shared.decorators import check_method, model_exists

from .models import Category
from .serializers import CategorySerializer


@check_method('GET')
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()


@check_method('GET')
@model_exists([Category, 'category_slug'])
def category_detail(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()

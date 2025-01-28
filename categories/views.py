from .models import Category
from .serializers import CategorySerializer

# Create your views here.


# Create your views here.
def category_list(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()


def category_detail(request, name):
    category = Category.objects.get(slug=name)
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()

# Create your views here.
from django.views.decorators.http import require_GET

from .models import Platform
from .serializers import PlatformSerializer


# Create your views here.
@require_GET
def platform_list(request):
    plataform = Platform.objects.all()
    serializer = PlatformSerializer(plataform, request=request)
    return serializer.json_response()


@require_GET
def platform_detail(request, name):
    plataform = Platform.objects.get(slug=name)
    serializer = PlatformSerializer(plataform, request=request)
    return serializer.json_response()

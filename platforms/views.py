# Create your views here.
from django.views.decorators.http import require_GET

from shared.decorators import check_method, existatata

from .models import Platform
from .serializers import PlatformSerializer



@check_method('GET')
@require_GET
def platform_list(request):
    plataform = Platform.objects.all()
    serializer = PlatformSerializer(plataform, request=request)
    return serializer.json_response()

@check_method('GET')
@existatata(Platform)
@require_GET
def platform_detail(request, slug):
    plataform = Platform.objects.get(slug=slug)
    serializer = PlatformSerializer(plataform, request=request)
    return serializer.json_response()

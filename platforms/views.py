
from django.views.decorators.http import require_GET

from shared.decorators import check_method, model_exists

from .models import Platform
from .serializers import PlatformSerializer


@check_method('GET')
@require_GET
def platform_list(request):
    plataform = Platform.objects.all()
    serializer = PlatformSerializer(plataform, request=request)
    return serializer.json_response()


@check_method('GET')
@model_exists([Platform, 'platform_slug'])
@require_GET
def platform_detail(request, platform_slug):
    plataform = Platform.objects.get(slug=platform_slug)
    serializer = PlatformSerializer(plataform, request=request)
    return serializer.json_response()

import re

from django.http import JsonResponse


def token_checker(func):
    def wrapper(request, *args, **kwargs):
        PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
        token = request.headers.get('Authorization')
        clean_token = re.fullmatch(PATTERN, token)
        if not clean_token:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


def check_method(func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return func(request, *args, **kwargs)

    return wrapper


def existatata(model):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                name = model._meta.object_name
                model.objects.get(slug=kwargs.get('slug'))
            except model.DoesNotExist:
                return JsonResponse({'error': f'{name} not found'}, status=404)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator

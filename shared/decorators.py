import json
import re

from django.http import JsonResponse

from users.models import Token


def token_checker(func):
    def wrapper(request, *args, **kwargs):
        PATTERN = r'^Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$'
        token = request.headers.get('Authorization')
        clean_token = re.fullmatch(PATTERN, token)
        if not clean_token:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)
        try:
            Token.objects.get(key=clean_token['token'])
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
        return func(request, *args, **kwargs)

    return wrapper


def json_checker(func):
    def wrapper(request, *args, **kwargs):
        try:
            json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


def field_checker(field_names):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                if len(field_names) != 1:
                    for field_name in field_names:
                        json.loads(request.body)[field_name]
                else:
                    json.loads(request.body)[field_names[0]]
            except KeyError:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def check_method(method):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != method:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def model_exists(list):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            model = list[0]
            slug_or_pk = list[1]
            try:
                name = model._meta.object_name
                if slug_or_pk == 'pk':
                    model.objects.get(pk=kwargs.get(slug_or_pk))
                else:
                    model.objects.get(slug=kwargs.get(slug_or_pk))
            except model.DoesNotExist:
                return JsonResponse({'error': f'{name} not found'}, status=404)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator

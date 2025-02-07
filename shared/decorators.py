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
            Token.objects.get(key=clean_token[1])
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


def rating_checker(func):
    def wrapper(request, *args, **kwargs):
        rating = json.loads(request.body)['rating']
        if rating not in list(range(1, 6)):
            return JsonResponse({'error': 'Rating is out of range'}, status=400)
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
                    json.loads(request.body)[field_names]
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


def existatata2(model):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                name = model._meta.object_name
                model.objects.get(pk=kwargs.get('pk'))
            except model.DoesNotExist:
                return JsonResponse({'error': f'{name} not found'}, status=404)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator

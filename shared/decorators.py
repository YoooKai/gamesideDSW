import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework import status

from categories.models import Category
from games.models import Game


def auth_required(func):
    def wrapper(request, *args, **kwargs):
        json_post = json.loads(request.body)
        try:
            user = get_user_model().objects.get(token_key=json_post['token'])
            request.user = user
        except get_user_model().DoesNotExist:
            return HttpResponse(status=status.UNAUTHORIZED)
        return func(request, *args, **kwargs)

    return wrapper


def check_method(func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return func(request, *args, **kwargs)

    return wrapper


def game_exist(func):
    def wrapper(request, *args, **kwargs):
        try:
            Game.objects.get(slug=args[1])
        except get_user_model().DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper


def category_exist(func):
    def wrapper(request, *args, **kwargs):
        try:
            Category.objects.get(slug=kwargs.get('slug'))
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
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

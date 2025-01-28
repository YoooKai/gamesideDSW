import json
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import status

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
# Create your views here.


import json

from django.contrib.auth import authenticate
from django.http import JsonResponse

from shared.decorators import check_method, json_checker,field_checker

@check_method('POST')
@json_checker
@field_checker(('password','username'))
def auth(request):
    username, password = json.loads(request.body).values()
    print(password)
    if user := authenticate(username=username, password=password):
        return JsonResponse({'token': user.token.key})
    return JsonResponse({'error': 'Invalid credentials'}, status=401)

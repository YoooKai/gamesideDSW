import json
from django.http import JsonResponse

def rating_checker(func):
    def wrapper(request, *args, **kwargs):
        rating = json.loads(request.body)['rating']
        if rating not in list(range(1, 6)):
            return JsonResponse({'error': 'Rating is out of range'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


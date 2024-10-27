from django.shortcuts import render

# Create your views here.
# api/views.py
from django.http import JsonResponse

def simple_json_view(request):
    data = {
        "message": "Hello, this is a simple JSON response!",
        "status": "success"
    }
    return JsonResponse(data)

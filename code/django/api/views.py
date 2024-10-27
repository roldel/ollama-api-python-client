from django.shortcuts import render

# Create your views here.
# api/views.py
from django.http import JsonResponse

def simple_json_view(request):
    data = {
        "weather report": """ 
        
        Weather Forecast for Bourges Over the Next 3 Days

        This Evening:
        At 4:00 PM, atmospheric pressure at sea level is 1022 hPa. Sunny and clear skies are expected. Temperature around 15°C at 7:00 PM. Light wind.

        Tonight:
        Fog banks are expected. Temperature around 12°C at 2:00 AM. Light and variable winds.

        Monday Morning:
        Mist expected. Temperature around 12°C at 7:00 AM. Light wind.

        Monday Afternoon:
        Clouds often obscuring the sun. Temperature around 16°C at 1:00 PM. Light and variable winds.

        Tuesday Morning:
        After fog clears in the morning, generally sunny. Minimum temperatures around 11°C. Light wind.

        Tuesday Afternoon:
        Generous sunshine. Maximum temperatures around 19°C. Light and variable winds.

        Wednesday Morning:
        Mist dissipating during the morning, followed by clear skies. Minimum temperatures around 11°C. Light east wind.

        Wednesday Afternoon:
        Sunny and clear weather. Maximum temperatures around 18°C. Light to moderate east wind.
        
        """,
        "status": "success"
    }
    return JsonResponse(data)

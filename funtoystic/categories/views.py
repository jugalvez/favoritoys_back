from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from utils.common import send_response, get_params
from .models import Category

@require_http_methods(["GET"])
def get_categories(request):
    categories = Category.objects.all().values_list('name', flat=True)

    response = {
        "message": "Categories fetched successfully",
        "data": list(categories)
    }

    return send_response(response, 200)
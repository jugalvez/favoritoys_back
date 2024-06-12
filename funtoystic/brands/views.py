from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from utils.common import send_response
from .models import Brand

@require_http_methods(["GET"])
def get_brands(request):
    brands = Brand.objects.all()

    response = {
        "message": "Brands fetched successfully",
        "data": brands
    }

    return send_response(response, 200)
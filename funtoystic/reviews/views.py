from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Avg

from utils.common import send_response
from .models import Review

@csrf_exempt
@require_POST
def create_review(request):
    rate = request.POST.get('rate')
    comments = request.POST.get('comments')

    review = Review(rate=rate, comments=comments)
    review.save()

    # Return a response indicating success
    response = {
        "message": "Review created successfully",
        "data": {}
    }
    return send_response(response, 200)


def get_average_review(request):
    # Calculate the average rate using Django's ORM
    product_id = request.GET.get('product_id')
    average_rate = Review.objects.filter(product_id=product_id).aggregate(Avg('rate'))['rate__avg']
    
    # Return the average rate as a JSON response
    response = {
        "message": "Average rate fetched",
        "data": {'average_rate': average_rate}
    }

    return send_response(response, 200)
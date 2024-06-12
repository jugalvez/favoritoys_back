from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from utils.common import send_response
from .models import Order


def order_create(request):
    order = Order.objects.create(
        name=request.data.get('name'),
        quantity=request.data.get('quantity'),
    )

    response = {
        "message": "Orders created successfully",
        "data": {'order': order}
    }

    return send_response(response, 200)


def order_list(request):
    orders = Order.objects.filter(user=request.user)

    response = {
        "message": "Orders fetched successfully",
        "data": {'orders': orders}
    }

    return send_response(response, 200)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    response = {
        "message": "Orders fetched successfully",
        "data": {'order': order}
    }

    return send_response(response, 200)
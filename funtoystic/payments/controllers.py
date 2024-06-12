from .models import Order

def update_order_status(order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Paid'
    order.save()

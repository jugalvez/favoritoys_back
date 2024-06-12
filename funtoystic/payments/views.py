from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.views.decorators.http import require_POST
from utils.common import send_response
from .controllers import update_order_status

# Configura tu clave secreta de Stripe
stripe.api_key = 'tu_clave_secreta_de_stripe'


@csrf_exempt
def process_payment(request):
    response = {
        "message": "Payment successful",
        "data": {}
    }

    if request.method == 'POST':
        # Obtén el token de pago y el monto desde la solicitud POST
        token = request.POST.get('token')
        amount = request.POST.get('amount')
        try:
            # Crea una carga en Stripe utilizando el token y el monto
            charge = stripe.Charge.create(
                amount=amount,
                currency='mxn',
                source=token
            )

            # El pago se ha procesado correctamente
            order_id = request.POST.get('order_id')
            update_order_status(order_id)

            return send_response(response, 200)

        except stripe.error.CardError as e:
            return send_response(None, 405)
        except Exception as e:
            return send_response(None, 400)
    else:
        return send_response(None, 400)
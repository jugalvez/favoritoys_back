import stripe
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse

class PaymentProcessTestCase(TestCase):
    def setUp(self):
        self.url = reverse('process_payment')
        self.token = 'test_token'
        self.amount = '1000'
        self.order_id = '12345'

    def test_payment_success(self):
        # Mock the Charge.create method to return a successful charge
        stripe.Charge.create = lambda **kwargs: {'status': 'succeeded'}

        response = self.client.post(self.url, {
            'token': self.token,
            'amount': self.amount,
            'order_id': self.order_id
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'message': 'Payment successful',
            'data': {}
        })

        # Assert that the order status was updated
        self.assertTrue(order_status_updated(self.order_id))

    def test_payment_card_error(self):
        # Mock the Charge.create method to raise a CardError
        stripe.Charge.create = lambda **kwargs: raise stripe.error.CardError('Card declined', 'card_declined')

        response = self.client.post(self.url, {
            'token': self.token,
            'amount': self.amount,
            'order_id': self.order_id
        })

        self.assertEqual(response.status_code, 405)
        self.assertIsNone(response.json())

    def test_payment_exception(self):
        # Mock the Charge.create method to raise an exception
        stripe.Charge.create = lambda **kwargs: raise Exception('Something went wrong')

        response = self.client.post(self.url, {
            'token': self.token,
            'amount': self.amount,
            'order_id': self.order_id
        })

        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.json())

    def test_invalid_request_method(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.json())

def order_status_updated(order_id):
    # Implement your logic to check if the order status was updated
    return True
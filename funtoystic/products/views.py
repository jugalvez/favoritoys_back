from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import boto3
from funtoystic.products.models import Product, ProductImage
from utils.common import send_response

@csrf_exempt
def new_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        image_files = request.FILES.getlist('image')

        # Create a new product object
        product = Product(name=name, price=price, description=description)
        product.save()

        # Create product image objects for each image file
        for image_file in image_files:
            product_image = ProductImage(product=product, image=image_file)
            product_image.save()

        # Return a JSON response indicating success
        response = {
            "message": "Product created successfully",
            "data": {}
        }

        return send_response(response, 200)

    # Return a JSON response indicating an error for other request methods
    return send_response(None, 405)


def update_product(request, product_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image_files = request.FILES.getlist('image')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        product.name = name
        product.price = price
        product.description = description
        product.save()

        for image_file in image_files:
            # Create an S3 client
            s3 = boto3.client('s3')

            for image_file in image_files:
                # Generate a unique key for the image file
                key = f'product_images/{product_id}/{image_file.name}'
                
                # Upload the image file to S3
                s3.upload_fileobj(image_file, 'your-bucket-name', key)
                
                # Create a product image object and save it
                product_image = ProductImage(product=product, image_url=f'https://your-bucket-name.s3.amazonaws.com/{key}')
                product_image.save()

        response = {
            "message": "Product updated successfully",
            "data": {}
        }
        return send_response(response, 200)

    return send_response(None, 405)


def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return send_response(None, 404)

        product.delete()

        response = {
            "message": "Product deleted successfully",
            "data": {}
        }

        return send_response(response, 200)

    return send_response(None, 405)


def get_product(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)

        product_ = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'images': [image.image_url for image in product.productimage_set.all()]
        }

        response = {
            "message": "Product detail",
            "data": {'product_': product_}
        }

        return send_response(response, 200)

    return send_response(None, 405)


def get_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_data = []

        for product in products:
            product_data.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'images': [image.image_url for image in product.productimage_set.all()]
            })

        response = {
            "message": "Product list",
            "data": {'product_data': product_data}
        }

        return send_response(response, 200)

    return send_response(None, 405)
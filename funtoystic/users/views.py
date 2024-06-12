from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse

def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        user_list = [{'id': user.id, 'username': user.username} for user in users]
        return JsonResponse(user_list, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def user_detail(request, pk):
    if request.method == 'GET':
        user = get_object_or_404(User, pk=pk)
        user_data = {'id': user.id, 'username': user.username}
        return JsonResponse(user_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Create a new user object
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Save the user object
        user.save()
        
        return JsonResponse({'message': 'User created'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'PUT':
        # Process the form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Update the user object
        user.username = username
        user.email = email
        
        # Save the updated user object
        user.save()
        
        return JsonResponse({'message': 'User updated'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'DELETE':
        # Soft delete the user object
        user.is_active = False
        user.save()        
        return JsonResponse({'message': 'User deleted'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

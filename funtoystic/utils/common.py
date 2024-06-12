from urllib import request
from django.http import JsonResponse
import json


def send_response(data, code=200):
    print("******** Response ********")
    print(code)
    print(data)
    print("**************************")

    status = {
        200: 'success',
        400: 'error',
        404: 'error',
        405: 'error',
    }

    errors = {
        400: 'Bad Request',
        404: 'Not Found',
        405: 'Method Not Allowed',
    }

    send_resp = json.JSONDecoder().decode(json.dumps(data, default=str))
    send_resp = JsonResponse(send_resp)

    # Make response template

    response = {
        "status_code": code,
        "status": status[code],
        "message": errors[code] if code in errors else send_resp.message,
        "data": send_resp.data if data else None
    }

    return response


def get_params():
    password = None
    params = request.get_json()
    print ("***********PARAMS************")

    if isinstance(params, dict):
        password = params.get('password', None)
        if password:
            params['password'] = '*'*len(password)

    print (str(params))
    
    if password:
        params['password'] = password
    print ("*******************************")
    return params

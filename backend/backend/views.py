from django.conf import settings
import json
from django.http import HttpResponse
from rest_framework import status
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import requests as r
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes
from .helpers import get, post, patch, put, delete, validate_proxy

status_codes = {200: status.HTTP_200_OK,
                201: status.HTTP_201_CREATED,
                204: status.HTTP_204_NO_CONTENT,
                400: status.HTTP_400_BAD_REQUEST,
                401: status.HTTP_401_UNAUTHORIZED,
                403: status.HTTP_403_FORBIDDEN,
                404: status.HTTP_404_NOT_FOUND,
                405: status.HTTP_405_METHOD_NOT_ALLOWED,
                409: status.HTTP_409_CONFLICT,
                500: status.HTTP_500_INTERNAL_SERVER_ERROR,
                503: status.HTTP_503_SERVICE_UNAVAILABLE}

responses = {200: {"success": "OK!"},
             201: {"success": "Successfully Created!"},
             204: {"success": "Successfully Deleted!"},
             400: {"error": "Bad Request!"},
             401: {"error": "Unauthorized!"},
             403: {"error": "Forbidden!!"},
             404: {"error": "Not Found!"},
             405: {"error": "Method Not Allowed!"},
             409: {"error": "Conflict!"},
             500: {"error": "Internal Server Error!"},
             503: {"error": "Service Unavailable!"}}


def get_headers(request):
    headers = {"Content-Type": request.headers.get("Content-Type", default="application/json")}
    if "X-CSRFToken" in request.headers:
        headers["X-CSRFToken"] = request.headers.get("X-CSRFToken")
    if "Authorization" in request.headers:
        headers["Authorization"] = request.headers.get("Authorization")
    return headers


def proxy_get(url_str, request):
    res = get(url_str, params=request.query_params, headers=get_headers(request))
    content_type = res.headers.get("Content-Type", default="application/json")
    if content_type == "application/json":
        status_code = status_codes[res.status_code]
        response_body = res.json() if res.status_code == 200 else responses[res.status_code]
        return status_code, content_type, response_body
    return status_codes[res.status_code], content_type, res.content


def proxy_put(url_str, request):
    res = put(url_str, data=json.dumps(request.data), headers=get_headers(request))
    content_type = res.headers.get("Content-Type", default="application/json")
    status_code = status_codes[res.status_code]
    response_body = res.json() if res.status_code in [200, 201] else responses[res.status_code]
    return status_code, content_type, response_body


def proxy_patch(url_str, request):
    res = patch(url_str, data=json.dumps(request.data), headers=get_headers(request))
    content_type = res.headers.get("Content-Type", default="application/json")
    status_code = status_codes[res.status_code]
    response_body = res.json() if res.status_code == 200 else responses[res.status_code]
    return status_code, content_type, response_body


def proxy_post(url_str, request):
    res = post(url_str, data=json.dumps(request.data), headers=get_headers(request))
    content_type = res.headers.get("Content-Type", default="application/json")
    status_code = status_codes[res.status_code]
    response_body = res.json() if res.status_code in [201, 200] else responses[res.status_code]
    return status_code, content_type, response_body


def proxy_delete(url_str, request):
    res = delete(url_str, headers=get_headers(request))
    content_type = res.headers.get("Content-Type", default="application/json")
    status_code = status_codes[res.status_code]
    response_body = responses[res.status_code]
    return status_code, content_type, response_body


def proxy_selector(request, proxy_url):
    if request.method == "PUT":
        return proxy_put(proxy_url, request)
    elif request.method == "GET":
        return proxy_get(proxy_url, request)
    elif request.method == "POST":
        return proxy_post(proxy_url, request)
    elif request.method == "DELETE":
        return proxy_delete(proxy_url, request)
    elif request.method == "PATCH":
        return proxy_patch(proxy_url, request)


@csrf_exempt
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
@api_view(['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
def proxy_requests(request, path):
    try:  # If Path Is A URL, We Need To Make A Request To Another Server
        validate = URLValidator()
        validate(path)
        path = path.replace("http:/", "http://")
        path = path.replace("https:/", "http://")
        path = path.replace("///", "//")
        if "followers" in path or "following" in path:
            parts = (path + "/").split("/")
            i = parts.index("authors") + 1
            j = parts.index("followers" if "followers" in path else "following")
            url = "/".join(parts[0:i+1]) + "/" + "/".join(parts[j:])
            if len(parts) - j > 4 and url[-2:] != "//":
                url += "/"
        else:
            if "http://" in path:
                url = "http://" + (path + "/").split("http://")[-1].replace("//", "/")
            else:
                url = "http://" + (path + "/").split("https://")[-1].replace("//", "/")
        status_code, content_type, response_body = proxy_selector(request, url)
        response_body = validate_proxy(response_body)
        if "application/json" not in content_type:
            response = HttpResponse(content_type=content_type, status=status_code)
            response.write(response_body)
            return response
        return Response(response_body, status=status_code, content_type="application/json")
    except ValidationError:  # If Path Is Not A URL, We Make The Request To Our Own Server
        status_code, content_type, response_body = proxy_selector(request, f"{settings.DOMAIN}/api/authors/{path}/")
        if content_type != "application/json":
            response = HttpResponse(content_type=content_type, status=status_code)
            response.write(response_body)
            return response
        return Response(response_body, status=status_code, content_type="application/json")


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def get_authors(request):
    res = r.get(f"{settings.DOMAIN}/api/authors", headers=get_headers(request), params=request.query_params)
    return Response(res.json(), status=status_codes[res.status_code])

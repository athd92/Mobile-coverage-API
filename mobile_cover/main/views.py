from django.shortcuts import render
from django.http import HttpResponse
from .address import Address
from django.http import JsonResponse
from main.models import Cover
from django.core import serializers


def get_coverage(request):
    """
    Main view function used convert query in Json response
    """
    if request.method == "GET":
        try:
            query = request.GET.get("q")  # fetch string url content

            query = Address(query)  # instance Address class obj
            coordonates = query.get_geoloc()  # use of Adrress class method
            result = query.get_result()

            if result == {}:
                return JsonResponse({"result": "no mathing found"})
            else:
                return JsonResponse(result)  # returns the final result
        except:
            return JsonResponse({"result": "no matching result found"})
    else:
        return JsonResponse({"result": "no matching result found"})


def error_404_view(request, exception):
    '''
    Error view function that returns a custom json if query
    is not understood
    '''
    return JsonResponse({"result": "syntax error"})

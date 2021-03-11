
from django.http import JsonResponse, request
from .sklad_exceptions import DataTypeError


class Middleware:
    def __init__(self, get_response): # def middleware(get_response)
        self.get_response = get_response
        # возвращается созданный объект, он возвращаемый, потому что __call__

    def __call__(self, request): #def middleware_callable(request)
        rs = self.get_response(request)
        return rs

    def process_exception(self, reqest, exception):
        if isinstance(exception, DataTypeError):
            # print("response from Middlewares")
            return JsonResponse({"DataTypeError": "object is not dict"}, status=404)

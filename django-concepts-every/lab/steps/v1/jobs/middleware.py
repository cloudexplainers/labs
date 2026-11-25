from django.db import connection


class QueryCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        before = len(connection.queries)
        response = self.get_response(request)
        response["X-Queries"] = len(connection.queries) - before
        return response

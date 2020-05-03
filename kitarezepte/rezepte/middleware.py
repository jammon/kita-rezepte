# -*- coding: utf-8 -*-
from .utils import get_client
from .models import Client


def subdomain_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.client_slug = get_client(request)
        try:
            request.client = Client.objects.get(slug=request.client_slug)
        except Client.DoesNotExist:
            request.client = None

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware

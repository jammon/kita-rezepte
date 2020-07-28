# -*- coding: utf-8 -*-
from .models import Domain


def subdomain_middleware(get_response):

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        domain_name = request.get_host().split(':')[0]
        try:
            domain = (Domain.objects
                      .select_related('provider', 'provider__client')
                      .get(domain=domain_name))
            request.provider = domain.provider
            request.client = domain.provider.client
        except Domain.DoesNotExist:
            request.provider = None
            request.client = None

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware

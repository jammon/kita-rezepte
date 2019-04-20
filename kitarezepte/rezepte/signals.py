from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

# from .models import Client


# @receiver(user_logged_in)
# def write_client_id_to_session(sender, **kwargs):
#     request = kwargs['request']
#     user = kwargs['user']
#     editor = user.editor
#     request.session['client_id'] = editor.client_id
#     request.session['user_name'] = user.get_full_name() or user.get_username()

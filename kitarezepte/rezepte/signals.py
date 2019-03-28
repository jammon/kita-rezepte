from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

# from .models import Ward


# @receiver(user_logged_in)
# def write_client_id_to_session(sender, **kwargs):
#     request = kwargs['request']
#     user = kwargs['user']
#     employee = user.employee
#     request.session['company_id'] = employee.company_id
#     request.session['department_ids'] = list(
#         employee.departments.values_list('id', flat=True))
#     request.session['can_config'] = user.has_perm('sp_app.add_person')
#     request.session['user_name'] = user.get_full_name() or user.get_username()
#     # User with editing rights should have their sessions expired
#     # when the browser is closed.
#     # They can change their passwords
#     if (user.has_perm('sp_app.add_changelogging') or
#             user.has_perm('sp_app.add_person')):
#         request.session.set_expiry(0)
#         request.session['can_change_password'] = True

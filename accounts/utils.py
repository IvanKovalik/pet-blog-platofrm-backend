import typing
from datetime import timedelta

from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from django_project.settings import EMAIL_HOST

_code_ttl = timedelta(minutes=5)


def send_verify_email(to_mail: str, code: str, subject: str = _("Verify Email")):
    html_content = _(
        "You are resetting the password, the verification code is：%(code)s, valid within 5 minutes, please keep it "
        "properly") % {'code': code}
    send_mail(recipient_list=[to_mail], subject=subject, message=html_content, from_email=EMAIL_HOST)


def verify(email: str, code: str) -> typing.Optional[str]:
    cache_code = get_code(email)
    if cache_code != code:
        return gettext("Verification code error")


def set_code(email: str, code: str):
    cache.set(email, code, _code_ttl.seconds)


def get_code(email: str) -> typing.Optional[str]:
    return cache.get(email)

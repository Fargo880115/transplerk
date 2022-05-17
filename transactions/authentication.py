import datetime
from django.utils.timezone import utc
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):

        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        utc_now = datetime.datetime.utcnow()

        if token.created.now() < utc_now - datetime.timedelta(hours=24):
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token

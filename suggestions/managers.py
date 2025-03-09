import hmac
import hashlib
from django.conf import settings
from django.db import models


def generate_anonymous_token(user_id: str) -> str:
    secret_key = settings.ANONYMOUS_SECRET_KEY.encode()
    message = str(user_id).encode()
    return hmac.new(secret_key, message, hashlib.sha256).hexdigest()

class SuggestionManager(models.Manager):
    def for_user(self, user):
        token = generate_anonymous_token(user.id)
        return self.filter(anon_token=token)

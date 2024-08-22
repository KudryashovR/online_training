from urllib.parse import urlparse

from rest_framework.exceptions import ValidationError


class LinkValidator:
    """
    Валидатор, который разрешает только ссылки на youtube.com.
    """

    message = 'Можно добавлять только ссылки на youtube.com.'

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        parsed_url = urlparse(value)

        if parsed_url.netloc != 'www.youtube.com' and parsed_url.netloc != 'youtube.com':
            raise ValidationError(self.message)

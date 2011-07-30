from __future__ import absolute_import

from django.conf import settings
from redis import Redis

redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
)

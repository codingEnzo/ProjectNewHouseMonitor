# coding = utf-8
from django.conf import settings


def sendSeed(key, value, host=settings.SEED_REDIS_CLIENT):
    host.sadd(key, value)

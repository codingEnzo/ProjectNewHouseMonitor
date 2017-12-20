# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseNantong


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoNantong


class PresellInfoItem(DjangoItem):
    django_model = PresellInfoNantong


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoNantong


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoNantong

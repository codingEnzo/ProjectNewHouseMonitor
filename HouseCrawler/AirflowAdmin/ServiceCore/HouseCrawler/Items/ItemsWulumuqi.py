# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseWulumuqi


class PresellInfoItem(DjangoItem):
    django_model = PresellInfoWulumuqi


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoWulumuqi


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoWulumuqi

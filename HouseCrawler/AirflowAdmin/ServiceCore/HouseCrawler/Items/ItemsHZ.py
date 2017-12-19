# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseHZ


class PresellInfoItem(DjangoItem):
    django_model = PresellInfoHZ


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoHZ


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoHZ


class IndexHouseInfoItem(DjangoItem):
    django_model = IndexHouseInfoHZ


class IndexInfoItem(DjangoItem):
    django_model = IndexInfoHZ

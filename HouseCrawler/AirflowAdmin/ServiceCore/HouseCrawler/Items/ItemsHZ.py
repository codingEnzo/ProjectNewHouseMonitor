# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseHangzhou


class PresellInfoItem(DjangoItem):
    django_model = PresellInfoHangzhou


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoHangzhou


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoHangzhou


class IndexHouseInfoItem(DjangoItem):
    django_model = IndexHouseInfoHangzhou


class IndexInfoItem(DjangoItem):
    django_model = IndexInfoHangzhou

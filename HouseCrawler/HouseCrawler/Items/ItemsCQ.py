# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBase


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfo


class HouseInfoItem(DjangoItem):
    django_model = HouseInfo

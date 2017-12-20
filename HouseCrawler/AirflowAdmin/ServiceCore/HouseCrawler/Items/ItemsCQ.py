# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseChongqing


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoChongqing


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoChongqing

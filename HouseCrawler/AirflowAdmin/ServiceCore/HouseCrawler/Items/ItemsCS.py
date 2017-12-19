# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseChangsha


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoChangsha


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoChangsha


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoChangsha

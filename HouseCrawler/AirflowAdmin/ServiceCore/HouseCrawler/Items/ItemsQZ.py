# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseQuanzhou


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoQuanzhou


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoQuanzhou


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoQuanzhou

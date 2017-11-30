# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseGuiyang


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoGuiyang


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoGuiyang


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoGuiyang

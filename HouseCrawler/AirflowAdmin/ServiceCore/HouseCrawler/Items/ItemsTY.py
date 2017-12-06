# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseTaiyuan


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoTaiyuan


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoTaiyuan


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoTaiyuan

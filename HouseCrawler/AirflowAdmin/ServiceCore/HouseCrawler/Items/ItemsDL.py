# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseDalian


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoDalian


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoDalian


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoDalian

# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseDongguan


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoDongguan


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoDongguan


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoDongguan

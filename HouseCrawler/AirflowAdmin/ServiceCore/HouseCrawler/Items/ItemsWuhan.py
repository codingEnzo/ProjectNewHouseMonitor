# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseWuhan


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoWuhan


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoWuhan


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoWuhan


class SignInfoItem(DjangoItem):
    django_model = SignInfoWuhan

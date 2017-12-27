# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseJinan


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoJinan


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoJinan


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoJinan


class SignInfoItem(DjangoItem):
    django_model = SignInfoJinan

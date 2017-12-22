# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseJiujiang


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoJiujiang


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoJiujiang


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoJiujiang

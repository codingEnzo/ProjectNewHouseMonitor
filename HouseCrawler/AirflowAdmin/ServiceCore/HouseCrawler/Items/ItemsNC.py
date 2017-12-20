# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseNanchang


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoNanchang


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoNanchang


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoNanchang

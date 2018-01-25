# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseYantai


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoYantai


class PresellInfoItem(DjangoItem):
    django_model = PresellInfoYantai


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoYantai


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoYantai
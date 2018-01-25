# coding = utf-8
from HouseNew.models import *
from scrapy_djangoitem import DjangoItem


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseXian


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoXian


class PresaleLicenseInfoItem(DjangoItem):
    django_model = PresaleInfoXian


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoXian


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoXian

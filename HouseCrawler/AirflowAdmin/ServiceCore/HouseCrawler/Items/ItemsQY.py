# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseQingyuan


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoQingyuan


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoQingyuan


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoQingyuan


class CompanyInfoItem(DjangoItem):
    django_model = CompanyInfoQingyuan


class PreSellInfoItem(DjangoItem):
    django_model = PreSellInfoQingyuan


class IndexInfoItem(DjangoItem):
    django_model = IndexInfoQingyuan

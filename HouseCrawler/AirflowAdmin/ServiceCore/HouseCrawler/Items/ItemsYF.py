# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseYunfu


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoYunfu


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoYunfu


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoYunfu


class CompanyInfoItem(DjangoItem):
    django_model = CompanyInfoYunfu


class PreSellInfoItem(DjangoItem):
    django_model = PreSellInfoYunfu


class IndexInfoItem(DjangoItem):
    django_model = IndexInfoYunfu

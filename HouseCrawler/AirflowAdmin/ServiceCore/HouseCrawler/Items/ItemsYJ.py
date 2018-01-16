# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseYangjiang


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoYangjiang


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoYangjiang


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoYangjiang


class CompanyInfoItem(DjangoItem):
    django_model = CompanyInfoYangjiang


class PreSellInfoItem(DjangoItem):
    django_model = PreSellInfoYangjiang


class IndexInfoItem(DjangoItem):
    django_model = IndexInfoYangjiang
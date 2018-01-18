# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseHeyuan


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoHeyuan


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoHeyuan


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoHeyuan


class CompanyInfoItem(DjangoItem):
    django_model = CompanyInfoHeyuan


class PreSellInfoItem(DjangoItem):
    django_model = PreSellInfoHeyuan

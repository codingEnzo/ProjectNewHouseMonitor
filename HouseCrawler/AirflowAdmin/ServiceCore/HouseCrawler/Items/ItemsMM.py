# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseMaoming


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoMaoming


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoMaoming


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoMaoming


class CompanyInfoItem(DjangoItem):
    django_model = CompanyInfoMaoming


class PreSellInfoItem(DjangoItem):
    django_model = PreSellInfoMaoming


class IndexInfoItem(DjangoItem):
    django_model = IndexInfoMaoming

# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseZhaoqing


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoZhaoqing


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoZhaoqing


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoZhaoqing


class CompanyInfoItem(DjangoItem):
    django_model = CompanyInfoZhaoqing


class PreSellInfoItem(DjangoItem):
    django_model = PreSellInfoZhaoqing

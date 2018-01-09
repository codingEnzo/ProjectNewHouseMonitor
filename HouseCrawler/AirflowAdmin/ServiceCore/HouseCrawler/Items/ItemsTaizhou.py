# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseTaizhou


class PresellInfoItem(DjangoItem):
    django_model = PresellInfoTaizhou


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoTaizhou


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoTaizhou


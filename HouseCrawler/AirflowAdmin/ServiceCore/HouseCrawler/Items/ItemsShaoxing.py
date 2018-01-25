# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *



class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseShaoxing


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoShaoxing


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoShaoxing


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoShaoxing
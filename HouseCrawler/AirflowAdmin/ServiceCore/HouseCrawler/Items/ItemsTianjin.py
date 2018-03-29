# coding = utf-8
from HouseNew.models import *
from scrapy_djangoitem import DjangoItem


class ProjectInfoItem(DjangoItem):
    django_model = ProjectDetailTianjin


Project_Detail_Item = ProjectInfoItem


class BuildingInfoItem(DjangoItem):
    django_model = BuildingDetailTianjin


Building_Detail_Item = BuildingInfoItem


class HouseInfoItem(DjangoItem):
    django_model = HouseDetailTianjin


House_Detail_Item = HouseInfoItem

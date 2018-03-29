# coding = utf-8
from HouseNew.models import *
from scrapy_djangoitem import DjangoItem


class Project_Detail_Item(DjangoItem):
    django_model = ProjectDetailTianjin


class Building_Detail_Item(DjangoItem):
    django_model = BuildingDetailTianjin


class House_Detail_Item(DjangoItem):
    django_model = HouseDetailTianjin

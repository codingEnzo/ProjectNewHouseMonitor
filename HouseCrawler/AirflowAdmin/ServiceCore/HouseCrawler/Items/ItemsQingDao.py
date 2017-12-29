# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *

class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseQingdao

class PresellInfoItem(DjangoItem):
    django_model = PresellInfoQingdao

class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoQingdao

class HouseInfoItem(DjangoItem):
    django_model = HouseInfoQingdao

class IndexInfoItem(DjangoItem):
    django_model = IndexInfoQingdao




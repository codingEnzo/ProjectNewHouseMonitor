# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *



class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoXuzhou


class PresellInfoItem(DjangoItem):
    django_model = PresellInfoXuzhou

class HouseInfoItem(DjangoItem):
    django_model = HouseInfoXuzhou


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoXuzhou

class UnitshapeImageInfoItem(DjangoItem):
    django_model = UnitshapeImageInfoXuzhou
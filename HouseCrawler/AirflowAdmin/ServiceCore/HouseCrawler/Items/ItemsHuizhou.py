# coding = utf-8
from HouseNew.models import *
from scrapy_djangoitem import DjangoItem

class Project_Detail_Item(DjangoItem):
    django_model = Project_DetailHuizhou


class Building_Detail_Item(DjangoItem):
    django_model = Building_DetailHuizhou


class House_Detail_Item(DjangoItem):
    django_model = House_DetailHuizhou


class Certificate_Detail_Item(DjangoItem):
    django_model = Certificate_DetailHuizhou

class Monitor_Item(DjangoItem):
    django_model = web_countHuizhou
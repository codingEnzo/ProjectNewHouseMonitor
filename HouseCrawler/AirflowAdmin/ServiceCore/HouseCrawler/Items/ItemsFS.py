# coding = utf-8
from HouseNew.models import *
from scrapy_djangoitem import DjangoItem


class Project_Detail_Item(DjangoItem):
    django_model = ProjectDetailFoshan


class Building_Detail_Item(DjangoItem):
    django_model = BuildingDetailFoshan


class House_Detail_Item(DjangoItem):
    django_model = HouseDetailFoshan


class Certificate_Detail_Item(DjangoItem):
    django_model = CertificateDetailFoshan


class Monitor_Item(DjangoItem):
    django_model = WebCountFoshan

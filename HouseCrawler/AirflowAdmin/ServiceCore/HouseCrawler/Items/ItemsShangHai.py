# coding = utf-8
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseShanghai


class OpeningunitItem(DjangoItem):
    django_model = OpeningunitBaseShanghai


class BuildingItem(DjangoItem):
    django_model = BuildingBaseShanghai


class HouseItem(DjangoItem):
    django_model = HouseBaseShanghai

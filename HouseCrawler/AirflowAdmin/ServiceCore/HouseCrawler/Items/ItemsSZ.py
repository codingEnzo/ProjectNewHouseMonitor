# coding = utf-8
from scrapy_djangoitem import DjangoItem

from HouseNew.models import *


class ApprovalBaseItem(DjangoItem):
    django_model = ApprovalBaseSuzhou


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseSuzhou


class BuildingBaseItem(DjangoItem):
    django_model = BuildingBaseSuzhou


class HouseBaseItem(DjangoItem):
    django_model = HouseBaseSuzhou


class ProjectallItem(DjangoItem):
    django_model = ProjectallBaseSuzhou

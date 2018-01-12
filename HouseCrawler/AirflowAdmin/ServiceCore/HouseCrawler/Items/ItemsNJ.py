# -*- coding: utf-8 -*-
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseNanjing


class BuildingBaseItem(DjangoItem):
    django_model = BuildingBaseNanjing


class HouseBaseItem(DjangoItem):
    django_model = HouseBaseNanjing


class DeveloperBaseItem(DjangoItem):
    django_model = DeveloperBaseNanjing


class PresaleBaseItem(DjangoItem):
    django_model = PresaleBaseNanjing

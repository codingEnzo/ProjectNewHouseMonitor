# -*- coding: utf-8 -*-

from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoGuangzhou


class PresellInfoItem(DjangoItem):
    django_model = PresellInfoGuangzhou


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoGuangzhou


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoGuangzhou


class PermitInfoItem(DjangoItem):
    django_model = PermitInfoGuangzhou

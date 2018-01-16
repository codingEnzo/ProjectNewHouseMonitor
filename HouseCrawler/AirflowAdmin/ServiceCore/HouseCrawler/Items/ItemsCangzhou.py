# -*- coding: utf-8 -*-
#!/usr/bin/python
from scrapy_djangoitem import DjangoItem
from NewCangzhou.HouseCrawler.HouseAdmin.HouseNew.models import *

class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseCangzhou


class LandBaseItem(DjangoItem):
    django_model = LandBaseCangzhou


class PlanningBaseItem(DjangoItem):
    django_model = PlanningBaseCangzhou


class ConstructionBaseItem(DjangoItem):
    django_model = ConstructionBaseCangzhou


class ConstructionLandPlanningBaseItem(DjangoItem):
    django_model = ConstructionLandPlanningBaseCangzhou


class DeveloperBaseItem(DjangoItem):
    django_model = DeveloperBaseCangzhou


class PresaleBaseItem(DjangoItem):
    django_model = PresaleBaseCangzhou


class HouseBaseItem(DjangoItem):
    django_model = HouseBaseCangzhou



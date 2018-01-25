# -*- coding: utf-8 -*-
#!/usr/bin/python
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *
class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseWenzhou

class DeveloperBaseItem(DjangoItem):
    django_model = DeveloperBaseWenzhou

class BuildingBaseItem(DjangoItem):
    django_model = BuildingBaseWenzhou

class HouseBaseItem(DjangoItem):
    django_model = HouseBaseWenzhou
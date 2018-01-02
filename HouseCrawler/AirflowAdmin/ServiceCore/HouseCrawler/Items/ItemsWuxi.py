# -*- coding: utf-8 -*-
#!/usr/bin/python
from scrapy_djangoitem import DjangoItem
from HouseNew.models import *


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseWuxi

class HouseBaseItem(DjangoItem):
    django_model = HouseBaseWuxi

class DeveloperBaseItem(DjangoItem):
    django_model = DeveloperBaseWuxi

class MonitorProjectBaseItem(DjangoItem):
    django_model = MonitorProjectBaseWuxi

class MonitorHouseBaseItem(DjangoItem):
    django_model = MonitorHouseBaseWuxi
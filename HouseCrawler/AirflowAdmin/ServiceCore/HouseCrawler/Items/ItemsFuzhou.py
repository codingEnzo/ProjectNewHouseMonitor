# coding = utf-8
from scrapy_djangoitem import DjangoItem

from HouseNew.models import *

class SearchProjectBaseItem(DjangoItem):
    django_model = SearchProjectBaseFuzhou

class ProjectinfoBaseItem(DjangoItem):
    django_model = ProjectinfoBaseFuzhou

class ApprovalBaseItem(DjangoItem):
    django_model = ApprovalBaseFuzhou

class BuildingBaseItem(DjangoItem):
    django_model = BuildingBaseFuzhou

class HouseBaseItem(DjangoItem):
    django_model = HouseBaseFuzhou
# coding = utf-8
from scrapy_djangoitem import DjangoItem

from HouseNew.models import ProjectBaseChangzhou, ProjectInfoChangzhou, BuildingInfoChangzhou, HouseInfoChangzhou


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseChangzhou


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoChangzhou


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoChangzhou


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoChangzhou

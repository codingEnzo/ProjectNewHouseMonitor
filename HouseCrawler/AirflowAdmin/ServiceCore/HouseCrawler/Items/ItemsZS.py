# -*- coding: utf-8 -*-
try:
    from scrapy_djangoitem import DjangoItem
    from HouseNew.models import *

    class ProjectBaseItem(DjangoItem):
        django_model = ProjectBaseZhongshan

    class ProjectInfoItem(DjangoItem):
        django_model = ProjectInfoZhongshan

    class BuildingInfoItem(DjangoItem):
        django_model = BuildingInfoZhongshan

    class HouseInfoItem(DjangoItem):
        django_model = HouseInfoZhongshan

except Exception:
    import traceback
    traceback.print_exc()

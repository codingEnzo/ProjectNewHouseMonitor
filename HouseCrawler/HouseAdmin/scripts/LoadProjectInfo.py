# coding = utf-8
import json
import redis
import datetime
from HouseNew.models import *


def run():
    num = 0
    r = redis.Redis('10.30.1.20')
    cur = ProjectBase.objects.filter(ProjectURLCurTimeStamp__gte=str(datetime.datetime.now().date())).all()
    for item in cur:
        if datetime.datetime.now().hour >= 8 and int(item.ProjectSaleSum) == 0:
            continue
        project_info = {'source_url': item.ProjectURL,
                        'meta': {'PageType': 'ProjectInfo'}}
        project_info_json = json.dumps(project_info, sort_keys=True)
        r.sadd('HouseCrawler:start_urls:Default:Dongguan', project_info_json)
        num += 1
    print(num)

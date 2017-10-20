# coding = utf-8
import json
import redis
from HouseNew.models import *


def run():
    num = 0
    r = redis.Redis('10.30.1.20')
    cur = ProjectBase.objects.all()
    for item in cur:
        project_info = {'source_url': item.ProjectURL,
                        'meta': {'PageType': 'ProjectInfo'}}
        project_info_json = json.dumps(project_info)
        r.sadd('HouseCrawler:start_urls:Default', project_info_json)
        num += 1
    print(num)

# coding = utf-8
import json
import redis
from HouseNew.models import *


def run():
    num = 0
    r = redis.Redis('10.30.1.20')
    cur = BuildingInfo.objects.all()
    for item in cur:
        try:
            if item.BuildingURL:
                builfing_info = {'source_url': item.BuildingURL,
                                    'meta': {'PageType': 'HouseInfo',
                                                'ProjectName': item.ProjectName,
                                                'BuildingName': item.BuildingName}}
                builfing_info_json = json.dumps(builfing_info)
                r.sadd('HouseCrawler:start_urls:Default', builfing_info_json)
                num += 1
        except Exception:
            import traceback
            traceback.print_exc()
    print(num)

# coding = utf-8
import json
import redis
import datetime
from HouseNew.models import *


def run():
    num = 0
    r = redis.Redis('10.30.1.20')
    cur = BuildingInfo.objects.aggregate(*[{"$sort": {"CurTimeStamp": 1}},
                                             {'$group':
                                                 {'_id': "$BuildingUUID",
                                                  'ProjectName': {'$first': '$ProjectName'},
                                                  'ProjectUUID': {'$first': '$ProjectUUID'},
                                                  'BuildingName': {'$first': '$BuildingName'},
                                                  'BuildingUUID': {'$first': '$BuildingUUID'},
                                                  'BuildingURL': {'$first': '$BuildingURL'},
                                                  'BuildingURLCurTimeStamp': {'$first': '$BuildingURLCurTimeStamp'}
                                                 }
                                             }])

    for item in cur:
        try:
            if item['BuildingURL']:
                if item['BuildingURLCurTimeStamp'] >= str(datetime.datetime.now().date()):
                    builfing_info = {'source_url': item['BuildingURL'],
                                        'meta': {'PageType': 'HouseInfo',
                                                    'ProjectName': item['ProjectName'],
                                                    'BuildingName': item['BuildingName'],
                                                    'ProjectUUID': str(item['ProjectUUID']),
                                                    'BuildingUUID': str(item['BuildingUUID'])}}
                    builfing_info_json = json.dumps(builfing_info, sort_keys=True)
                    r.sadd('HouseCrawler:start_urls:Default:Chongqing', builfing_info_json)
                    num += 1
        except Exception:
            import traceback
            traceback.print_exc()
    print(num)

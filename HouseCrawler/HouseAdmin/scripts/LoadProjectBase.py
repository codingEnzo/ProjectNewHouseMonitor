# coding = utf-8
import json
import redis


def run():
    r = redis.Redis('10.30.1.20')
    project_base = {'source_url': 'http://www.cq315house.com/315web/HtmlPage/SpfQuery.htm',
                    'meta': {'PageType': 'ProjectBase'}}
    project_base_json = json.dumps(project_base, sort_keys=True)
    r.sadd('HouseCrawler:start_urls:Default:Chongqing', project_base_json)

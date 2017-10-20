# coding = utf-8
import json
import redis


def run():
    r = redis.Redis('10.30.1.20')
    project_base = {'source_url': 'http://www.bjjs.gov.cn/eportal/ui?pageId=307678&isTrue=',
                    'meta': {'PageType': 'ProjectBase'}}
    project_base_json = json.dumps(project_base)
    r.sadd('HouseCrawler:start_urls:Default', project_base_json)

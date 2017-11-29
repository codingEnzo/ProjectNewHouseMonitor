# coding = utf-8
import json
import redis


def run():
    r = redis.Redis('10.30.1.20')
    project_base = {'source_url': 'http://www.jjzzfdc.com.cn/WebClient/ClientService/frmSalesLPDisplay_more.aspx?qcount=10000&pcount=10000&Page=1',
                    'meta': {'PageType': 'ProjectBase'}}
    project_base_json = json.dumps(project_base, sort_keys=True)
    r.sadd('HouseCrawler:start_urls:Default:Jiujiang', project_base_json)

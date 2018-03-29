# coding = utf-8
import re
import sys
import uuid

from HouseCrawler.Items.ItemsTianjin import *
from scrapy import Request

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

clean_rule1 = lambda x: x.strip().replace('\r', "") if x else ''
clean_rule2 = lambda x: x.strip().replace('\n', ";").replace(
    '\r', "").replace('\t', '') if x else ''


def cheack_response(pagetype, response, result):
    if (response.meta.get('PageType') in pagetype) and (200 <= response.status < 303):
        out_come = 'right' if result else []
    else:
        out_come = result if result else []

    return out_come


class ProjectDetailMiddleware(object):
    headers = {"Referer": 'http://www.tjfdc.com.cn/Pages/fcdt/fcdtlist.aspx?SelMnu=FCSJ_XMXX',
               "Host": "www.tjfdc.com.cn",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Upgrade-Insecure-Requests": "1",
               'Content-Type': 'application/x-www-form-urlencoded',
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        out_come = cheack_response(
            pagetype=['pl_url', 'pd_url'], response=response, result=result)
        pagetype = response.meta['PageType']
        outcome_list = []
        if (out_come == 'right') and (pagetype == 'pl_url'):
            contentli = response.xpath('//*[@id="divContent"]/ul/li')
            for i in contentli:
                item = Project_Detail_Item()
                item['ProjectName'] = clean_rule1(
                    i.xpath('.//div[2]/div[1]/h3/a/text()').extract_first())
                item['RegionName'] = clean_rule1(
                    i.xpath('.//div[2]/div[2]/table/tbody/tr[2]/td[2]/text()').extract_first())
                Project_raw = item['ProjectName'] + item['RegionName']
                item['ProjectUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, Project_raw)
                item['HouseUseHousingPrice'] = clean_rule1(
                    i.xpath('.//div[2]/div[2]/table/tbody/tr[1]/td[2]/span[1]/text()').extract_first())
                item['HouseUseNonhousingPrice'] = clean_rule1(
                    i.xpath('.//div[2]/div[2]/table/tbody/tr[1]/td[2]/span[2]/text()').extract_first())
                item['TotalBuidlingArea'] = clean_rule1(
                    i.xpath('.//div[2]/div[2]/table/tbody/tr[1]/td[4]/text()').extract_first())
                item['Developer'] = clean_rule1(
                    i.xpath('.//div[2]/div[2]/table/tbody/tr[1]/td[6]/text()').extract_first())
                item['ProjectAddress'] = clean_rule1(
                    i.xpath('.//div[2]/div[2]/table/tbody/tr[2]/td[6]/text()').extract_first())
                item['EarliestOpeningTime'] = clean_rule1(
                    i.xpath('.//div[2]/div[1]/span/text()').extract_first())
                item['ProjectUrl'] = 'http://www.tjfdc.com.cn/Pages/fcdt/' + clean_rule1(
                    i.xpath('.//div[2]/div[1]/h3/a/@href').extract_first())
                re_get = Request(url=item['ProjectUrl'], method='GET', headers=self.headers,
                                 meta={'PageType': 'pd_url', "item": item}, dont_filter=True)
                outcome_list.append(re_get)
            # ASP网站,到每一页获取参数post请求下一页
            pages_num = int(response.xpath(
                '//*[@id="SplitPageModule1_lblPageCount"]/text()').extract_first())
            now_pages_num = int(response.xpath(
                '//*[@id="SplitPageModule1_lblCurrentPage"]/text()').extract_first())
            if int(now_pages_num) < int(pages_num):
                post_url = 'http://www.tjfdc.com.cn/Pages/fcdt/fcdtlist.aspx?SelMnu=FCSJ_XMXX'
                re_postbody = {"__EVENTTARGET": 'SplitPageModule1$lbnNextPage',
                               "__EVENTARGUMENT": "",
                               "__VIEWSTATE": response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first(),
                               "__VIEWSTATEGENERATOR": response.xpath(
                                   '//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first(),
                               "__EVENTVALIDATION": response.xpath(
                                   '//*[@id="__EVENTVALIDATION"]/@value').extract_first(),
                               "hidDoing": "", "hidCountNow": "20", "hidPage": "1", "txtQy": "", "hidQy": "",
                               "txtXzqh": "", "hidXzqh": "", "txtBk": "", "hidBk": "", "txtProjecttype": "",
                               "hidProjecttype": "",
                               "txtXmmc": "", "txtKpzt": "", "hidKpzt": "", }
                projectList_req = Request(url=post_url, method='POST', headers=self.headers,
                                          body=urlparse.urlencode(re_postbody), meta={'PageType': 'pl_url'},
                                          dont_filter=True)
                outcome_list.append(projectList_req)
            return outcome_list
        elif (out_come == 'right') and (pagetype == 'pd_url'):
            item = response.meta['item']
            item['ProjectAddress'] = clean_rule1(response.xpath(
                '//*[@id="lblWYDZ"]/text()').extract_first())
            item['ProjectTradeArea'] = clean_rule1(
                response.xpath('//*[@id="lblSSSQ"]/text()').extract_first())
            item['Project_PlanType'] = clean_rule1(response.xpath(
                '//*[@id="lblPLANTYPE"]/text()').extract_first())
            item['FloorAreaRatio'] = clean_rule1(response.xpath(
                '//*[@id="lblRJL"]/text()').extract_first())
            item['GreeningRate'] = clean_rule1(response.xpath(
                '//*[@id="lblGREENPROP"]/text()').extract_first())
            item['EarliestOpeningTime'] = clean_rule1(
                response.xpath('//*[@id="lblKPSJ"]/text()').extract_first())
            item['BuildingStructure'] = clean_rule1(response.xpath(
                '//*[@id="lblSTRUCTURE"]/text()').extract_first())
            item['ManagementFees'] = clean_rule1(response.xpath(
                '//*[@id="lblWYF"]/text()').extract_first())
            item['ManagementCompany'] = clean_rule1(
                response.xpath('//*[@id="lblWYGS"]/text()').extract_first())
            item['Project_Type'] = clean_rule1(response.xpath(
                '//*[@id="lblWYLB"]/text()').extract_first())
            item['Project_Feature'] = clean_rule2(response.xpath(
                '//*[@id="lblXMTE"]/text()').extract_first())
            item['Project_Traffic'] = clean_rule2(response.xpath(
                '//*[@id="lblJTZK"]/text()').extract_first())
            item['Project_Introduce'] = clean_rule2(
                response.xpath('//*[@id="lblXMJS"]/text()').extract_first())
            item['Project_Surround'] = clean_rule2(
                response.xpath('//*[@id="lblZBPT"]/text()').extract_first())
            item['Project_BuildingInformation'] = clean_rule1(
                response.xpath('//*[@id="lblLCZK"]/text()').extract_first())
            item['ParkingSpaceAmount'] = clean_rule1(
                response.xpath('//*[@id="lblCWXX"]/text()').extract_first())
            item['Project_Information'] = clean_rule1(
                response.xpath('//*[@id="lblXGXX"]/text()').extract_first())
            item['TotalBuidlingArea'] = clean_rule1(response.xpath(
                '//*[@id="lblSUMBUILDAREA"]/text()').extract_first())
            item['FloorArea'] = clean_rule1(response.xpath(
                '//*[@id="lblSUMLANDAREA"]/text()').extract_first())
            outcome_list.append(item)
            return outcome_list
        else:
            return out_come

    def process_spider_exception(self, response, exception, spider):
        return


class ProjectGetFidMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    # 爬取时先通过搜索找到项目对应的fid值，
    def process_spider_output(self, response, result, spider):
        def getParamsDict(url):
            query = urlparse.urlparse(url).query
            return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])

        out_come = cheack_response(
            pagetype=['GetProjectFid'], response=response, result=result)
        if out_come == 'right':
            outcome_list, pagetype = [], response.meta['PageType']
            recorddata_dict = response.meta['Record_Data']
            # print('Record_Data:',recorddata_dict)
            content = response.xpath('//*[@id="divContent"]/ul/li')
            for i in content:
                projectname = clean_rule1(
                    i.xpath('./div[2]/div[1]/h3/a/text()').extract_first())
                regionName = clean_rule1(
                    i.xpath('./div[2]/div[2]/table/tbody/tr[2]/td[2]/text()').extract_first())
                if (projectname == recorddata_dict['ProjectName']) and (regionName == recorddata_dict['RegionName']):
                    url = i.xpath("./div[2]/div[1]/h3/a/@href").extract_first()
                    try:
                        fid = getParamsDict(url).get('fid', '')
                        # print('fid:{0}'.format(fid))
                        buildingList_req = Request(
                            url='http://www.tjfdc.com.cn/Pages/fcdt/LouDongList.aspx?selmnu=FCSJ_XMXX_LPB&fid={0}'.format(
                                fid),
                            meta={'PageType': 'BuildingList',
                                  'Record_Data': recorddata_dict},
                            dont_filter=True)
                        outcome_list.append(buildingList_req)
                    except:
                        import traceback
                        traceback.print_exc()
                    break
            return outcome_list
        else:
            return out_come


class BuildingDetailMiddleware(object):
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Cache-Control": "max-age=0",
               "Connection": "keep-alive",
               'Content-Type': 'application/x-www-form-urlencoded',
               "Host": "www.tjfdc.com.cn",
               "Origin": "http://www.tjfdc.com.cn",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        out_come = cheack_response(
            pagetype=['BuildingList'], response=response, result=result)

        if out_come == 'right':

            cheack_key = response.xpath(
                '//*[@id="form1"]/script/text()').re('此项目不存在')
            if cheack_key:
                print('此项目不存在')
                print(response.body_as_unicode())
            if not cheack_key:
                outcome_list, recorddata_dict = [], response.meta['Record_Data']

                bd_content = response.xpath('//tr[@style="height: 30px"]')
                for i in bd_content:
                    item_bd = Building_Detail_Item()
                    item_bd['SourceUrl'] = response.url
                    item_bd['ProjectName'] = recorddata_dict['ProjectName']
                    item_bd['RegionName'] = recorddata_dict['RegionName']
                    item_bd['ProjectUUID'] = recorddata_dict['ProjectUUID']
                    item_bd['BuildingName'] = clean_rule1(
                        i.xpath('./td[1]/span/text()').extract_first())
                    item_bd['BuildingNumber'] = clean_rule1(
                        i.xpath('string(./td[2]/a)').extract_first())
                    item_bd['SalePermitNumber'] = i.xpath(
                        './td[3]/span/text()').extract_first()
                    item_bd['OpeningTime'] = i.xpath(
                        './td[4]/span/text()').extract_first()
                    item_bd['HouseSalePrice'] = i.xpath(
                        './td[5]/span/text()').extract_first()
                    item_bd['HouseSalePrice_Not'] = i.xpath(
                        './td[6]/span/text()').extract_first()
                    item_bd['OnsoldAmount'] = i.xpath(
                        './td[7]/span/text()').extract_first()
                    BuildingUUID_raw = item_bd[
                        'ProjectUUID'] + item_bd['BuildingName'] + item_bd['BuildingNumber']
                    item_bd['BuildingUUID'] = uuid.uuid3(
                        uuid.NAMESPACE_DNS, BuildingUUID_raw)
                    # print('BuildingUUID:',str(item_bd['BuildingUUID']))
                    try:
                        item_bd['BuildingID'] = i.xpath(
                            './td[2]/a/@href').re("\('(.+?)\'")[0]
                    except Exception as e:
                        item_bd['BuildingID'] = ''
                    re_postbody = {"__EVENTTARGET": item_bd['BuildingID'],
                                   "__EVENTARGUMENT": "",
                                   "__VIEWSTATE": response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first(),
                                   "__VIEWSTATEGENERATOR": response.xpath(
                        '//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first(),
                        "__EVENTVALIDATION": response.xpath(
                        '//*[@id="__EVENTVALIDATION"]/@value').extract_first(),
                        "hidDoing": "", "txtJD": "", "txtWD": "", "txtProName": ""}
                    re_post = Request(url=response.url, method='POST', headers=self.headers,
                                      body=urlparse.urlencode(re_postbody),
                                      meta={'PageType': 'UnitList',
                                            'item': item_bd},
                                      dont_filter=True)
                    outcome_list.append(re_post)

                # 翻页
                pages_count = response.xpath(
                    '//*[@id="LouDongList1_SplitPageIconModule1_lblPageCount"]/text()').extract_first()
                now_pages_num = response.xpath(
                    '//*[@id="LouDongList1_SplitPageIconModule1_lblCurrentPage"]/text()').extract_first()
                if now_pages_num != pages_count:
                    post_url = response.url
                    re_postbody = {"__EVENTTARGET": "LouDongList1$SplitPageIconModule1$lbnNextPage",
                                   "__EVENTARGUMENT": "",
                                   "__VIEWSTATE": response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first(),
                                   "__VIEWSTATEGENERATOR": response.xpath(
                                       '//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first(),
                                   "__EVENTVALIDATION": response.xpath(
                                       '//*[@id="__EVENTVALIDATION"]/@value').extract_first(),
                                   "hidDoing": "", "txtJD": "", "txtWD": "", "txtProName": ""}
                    re_post = Request(url=post_url, method='POST', headers=self.headers,
                                      body=urlparse.urlencode(re_postbody),
                                      meta={'PageType': 'BuildingList',
                                            'Record_Data': recorddata_dict},
                                      dont_filter=True)
                    outcome_list.append(re_post)
                return outcome_list
            else:
                return out_come
        else:
            return out_come

    def process_spider_exception(self, response, exception, spider):
        return


class HouseDetailMiddleware(object):
    headers_post = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    'Content-Type': 'application/x-www-form-urlencoded',
                    "Host": "www.tjfdc.com.cn",
                    "Cookie": "ASP.NET_SessionId=ucuua55mygj4bgoeimoiitxf",
                    "Origin": "http://www.tjfdc.com.cn",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
                    }
    statetransferdict = {
        "background-color:#aade9c;": '未售',
        'background-color:#ff5e59;': '已售',
        'background-color:#fff28c;': '预定',
        'background-color:#a0a0a0;': '其它不可售房',
        'background-color:Gray;': '其它不可售房'

    }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(pagetype=['UnitList', 'HouseList', "HouseDetail"], response=response,
                                   result=result)
        outcome_list, pagetype = [], response.meta['PageType']
        if out_come == 'right':
            if pagetype == 'UnitList':  # 获取所有单元
                print('get UnitList')
                item_bd = response.meta.get('item')
                item_bd['HouseAmount'] = clean_rule2(
                    response.xpath('//*[@id="LouDongInfo1_lblHouseCount"]/text()').extract_first())
                outcome_list.append(item_bd)

                door_number = response.xpath(
                    '//*[@id="divLouDongInfo"]/div/div[2]/div/table/tr[2]/td/a')

                for i in door_number:
                    record_dict = {}
                    record_dict['BuildingUUID'] = str(item_bd['BuildingUUID'])
                    record_dict['ProjectUUID'] = str(item_bd['ProjectUUID'])
                    record_dict['BuildingName'] = item_bd['BuildingName']
                    record_dict['BuildingNumber'] = item_bd['BuildingNumber']
                    record_dict['ProjectName'] = item_bd['ProjectName']
                    record_dict['BuildingID'] = item_bd['BuildingID']
                    record_dict['SalePermitNumber'] = item_bd[
                        'SalePermitNumber']
                    record_dict['UnitID'] = i.xpath(
                        './@href').re("\('(.+?)\'")[0]
                    record_dict['UnitName'] = clean_rule1(
                        i.xpath("./text()").extract_first())
                    re_postbody = {"__EVENTTARGET": record_dict['UnitID'],
                                   "__EVENTARGUMENT": "",
                                   "__VIEWSTATE": response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first(),
                                   "__VIEWSTATEGENERATOR": response.xpath(
                        '//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first(),
                        "__EVENTVALIDATION": response.xpath(
                        '//*[@id="__EVENTVALIDATION"]/@value').extract_first(),
                        "hidDoing": "", "txtJD": "", "txtWD": "", "txtProName": ""}
                    HouseList_post = Request(url=response.url,
                                             method='POST',
                                             headers=self.headers_post,
                                             body=urlparse.urlencode(
                                                 re_postbody),
                                             meta={'PageType': 'HouseList',
                                                   'Record_Data': record_dict, },
                                             dont_filter=True)
                    outcome_list.append(HouseList_post)
                return outcome_list
            elif pagetype == 'HouseList':  # 解析户列表
                record_dict = response.meta['Record_Data']
                foor_list = response.xpath(
                    '//*[@id="LouDongInfo1_dgData"]/tr/td[contains(@style,"background")]')
                print('get HouseList,having {0} house'.format(len(foor_list)))
                for i in foor_list:
                    item_hd = House_Detail_Item()
                    item_hd['BuildingUUID'] = record_dict['BuildingUUID']
                    item_hd['ProjectUUID'] = record_dict['ProjectUUID']
                    item_hd['BuildingName'] = record_dict['BuildingName']
                    item_hd['BuildingNumber'] = record_dict['BuildingNumber']
                    item_hd['ProjectName'] = record_dict['ProjectName']
                    item_hd['BuildingID'] = record_dict['BuildingID']
                    item_hd['SalePermitNumber'] = record_dict[
                        'SalePermitNumber']
                    item_hd['UnitID'] = record_dict['UnitID']
                    item_hd['UnitName'] = record_dict['UnitName']
                    item_hd['FloorName'] = clean_rule1(
                        i.xpath('../td[contains(@style,"width")]/text()').extract_first())
                    item_hd['HouseName'] = clean_rule1(
                        (i.xpath('string(.)').extract_first()))
                    state = i.xpath('./@style').extract_first()
                    item_hd['HouseSaleState'] = self.statetransferdict.get(
                        state, state)
                    houseuuid_raw = item_hd['ProjectName'] + item_hd['BuildingName'] + item_hd['BuildingNumber'] + \
                        item_hd[
                        'UnitName'] + item_hd['HouseName'] + item_hd['SalePermitNumber']
                    item_hd['HouseUUID'] = str(uuid.uuid3(
                        uuid.NAMESPACE_DNS, houseuuid_raw))
                    # 判断是否有户详情链接
                    url_raw = i.xpath('./a/@onclick').extract_first()
                    if url_raw:
                        item_hd['HouseUrl'] = re.search(
                            r'\"(htt.+?)\"', url_raw).group(1)
                        reqget = Request(url=item_hd['HouseUrl'], method='GET', headers=self.headers_post,
                                         meta={'PageType': 'HouseDetail', "item": item_hd}, dont_filter=True)
                        outcome_list.append(reqget)
                    else:
                        item_hd['HouseUrl'] = ''
                        outcome_list.append(item_hd)
                return outcome_list
            elif pagetype == 'HouseDetail':  # 解析户详情页面
                print('get HouseDetail')
                item_hd = response.meta.get('item')
                item_hd['HouseUseType'] = response.xpath(
                    '//*[@id="lblUSE"]/text()').extract_first()
                item_hd['UnitShape'] = response.xpath(
                    '//*[@id="lblBUILDTYPE"]/text()').extract_first()
                item_hd['Toward'] = response.xpath(
                    '//*[@id="lblHOUSEDIRECTION"]/text()').extract_first()
                item_hd['FloorHight'] = response.xpath(
                    '//*[@id="lblFULLLAYER"]/text()').extract_first()
                item_hd['BuildingStructure'] = response.xpath(
                    '//*[@id="lblSTRUCTURE"]/text()').extract_first()
                item_hd['MeasuredBuildingArea'] = response.xpath(
                    '//*[@id="lblBUILDAREA"]/text()').extract_first()
                item_hd['MeasuredInsideOfBuildingArea'] = response.xpath(
                    '//*[@id="lblINTERAREA"]/text()').extract_first()
                item_hd['MeasuredSharedPublicArea'] = response.xpath(
                    '//*[@id="lblPUBLICAREA"]/text()').extract_first()
                item_hd['SalePriceByInsideOfBuildingArea'] = response.xpath(
                    '//*[@id="lblMMPRICE"]/text()').extract_first()
                outcome_list.append(item_hd)
                return outcome_list
        else:
            return out_come

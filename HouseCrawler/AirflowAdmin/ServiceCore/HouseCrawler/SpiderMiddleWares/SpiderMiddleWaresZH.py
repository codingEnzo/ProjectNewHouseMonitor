# coding = utf-8
import sys
import uuid
import re
from scrapy import Request
from HouseNew.models import *
from HouseCrawler.Items.Items import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

clean_rule1 = lambda x: x.strip().replace('\r', "") if x else ''
clean_rule2 = lambda x: x.strip().replace('\n', "").replace(
    '\r', "").replace('\t', '') if x else ''


def cheack_response(pagetype, response, result):

    if (response.meta.get('PageType') in pagetype) and (200 <= response.status < 303):

        out_come = 'right' if result else []

    else:
        out_come = result if result else []

    return out_come


class ProjectListMiddleware(object):

    headers = {"Referer": "https://61.143.53.130:4433/zhpubweb/projectQuery.aspx",
               "Host": "61.143.53.130:4433",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate,br",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               'Content-Type': 'application/x-www-form-urlencoded',
               'Origin': 'https://61.143.53.130:4433',
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
               }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(
            pagetype=['pl_url'], response=response, result=result)

        if out_come == 'right':

            outcome_list, pagetype, recorddata_dict = [], response.meta[
                'PageType'], response.meta['Record_Data']

            # print('ProjectGetFidMiddleware')

            crawler_type = recorddata_dict['crawler_type']

            page_text = response.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_pageInfo"]/text()').extract_first()

            pages_num = re.findall(r'共(.+?)页', page_text)[0]

            now_page_num = re.findall(r'第(.+?)页', page_text)[0]

            # print (now_page_num,pages_num)

            if int(now_page_num) < int(pages_num):

                re_postbody = {"__EVENTTARGET": 'ctl00$ContentPlaceHolder1$lnkBtnNext',
                               "__EVENTARGUMENT": "",
                               "__VIEWSTATE": response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first(),
                               "__EVENTVALIDATION": response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first(),
                               "ctl00$ContentPlaceHolder1$txtProjectName": "",
                               "ctl00$ContentPlaceHolder1$txtPreSaleCert": "",
                               "ctl00$ContentPlaceHolder1$txtDeveloper": "",
                               "ctl00$ContentPlaceHolder1$txtSitnumgather": "",
                               "ctl00$ContentPlaceHolder1$newpage": ""}

                post_url = "https://61.143.53.130:4433/zhpubweb/projectQuery.aspx"

                re_post = Request(url=post_url, method='POST', headers=self.headers, body=urlparse.urlencode(
                    re_postbody.copy()), meta={'PageType': 'pl_url', "Record_Data": recorddata_dict}, dont_filter=True)

                outcome_list.append(re_post)

            content = response.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_GridViewProjectQuery"]/tr')
            for i in content[1:]:

                item_pd = Project_Detail_Item()

                item_pd['ProjectName'] = clean_rule1(
                    i.xpath('./td[1]/text()').extract_first())

                item_pd['ProjectAddress'] = clean_rule1(
                    i.xpath('./td[2]/text()').extract_first())

                item_pd['PresalePermitNumber'] = clean_rule1(
                    i.xpath('./td[3]/text()').extract_first())

                item_pd['LssueDate'] = clean_rule1(
                    i.xpath('./td[4]/text()').extract_first())

                item_pd['PresaleHouseCount'] = clean_rule1(
                    i.xpath('./td[5]/text()').extract_first())

                item_pd['HouseUnsoldAmount'] = clean_rule1(
                    i.xpath('./td[6]/text()').extract_first())

                item_pd['SellState'] = clean_rule1(
                    i.xpath('./td[7]/text()').extract_first())

                item_pd['RealEstateProjectID'] = re.findall(r'recnumgather\=(.+)', i.xpath(
                    './td[8]/a/@href').extract_first())[0] if i.xpath('./td[8]/a/@href').extract_first() else ''

                item_pd['ProjectUrl'] = 'https://61.143.53.130:4433/zhpubweb/SaleMsg.aspx?recnumgather={0}'.format(
                    item_pd['RealEstateProjectID'])

                item_pd["PageNumber"] = now_page_num

                url_bd = item_pd['ProjectUrl']

                re_get2 = Request(url=url_bd, method='GET', meta={
                                  'PageType': 'pd_url', "Item": item_pd}, dont_filter=True)

                outcome_list.append(re_get2)

            return outcome_list

        else:

            return out_come

    def process_spider_exception(self, response, exception, spider):

        return


class ProjectDetailMiddleware(object):

    headers = {"Referer": "https://61.143.53.130:4433/zhpubweb/projectQuery.aspx",
               "Host": "61.143.53.130:4433",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate,br",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               'Content-Type': 'application/x-www-form-urlencoded',
               'Origin': 'https://61.143.53.130:4433',
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
               }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):

        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        # print('ProjectListMiddleware')

        out_come = cheack_response(
            pagetype=['pd_url'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        if out_come == 'right' and pagetype == 'pd_url':

            item_pd = response.meta['Item']

            item_pd['ProjectUUID'] = str(uuid.uuid3(
                uuid.NAMESPACE_DNS, item_pd['ProjectName']))

            item_pd['PresalePermitNumberUUID'] = str(uuid.uuid3(
                uuid.NAMESPACE_DNS, item_pd['ProjectName'] + item_pd['PresalePermitNumber']))

            item_pd['ApprovalPresaleAmount'] = clean_rule1(response.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr[not(@align)]/td[2]/text()').extract_first())

            item_pd['HouseUnsoldAmount'] = clean_rule1(response.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr[not(@align)]/td[3]/text()').extract_first())

            item_pd['HouseSoldAmount'] = clean_rule1(response.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr[not(@align)]/td[4]/text()').extract_first())

            item_pd['ApprovalPresaleArea'] = clean_rule1(response.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr[not(@align)]/td[5]/text()').extract_first())

            item_pd['UnsoldArea'] = clean_rule1(response.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr[not(@align)]/td[6]/text()').extract_first())

            item_pd['OnSoldArea'] = clean_rule1(response.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr[not(@align)]/td[7]/text()').extract_first())

            outcome_list.append(item_pd)

            content_bd = response.xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_GridView1"]/tr')

            for i in content_bd[1:-1]:

                item_bd = Building_Detail_Item()

                item_bd['SourceUrl'] = response.url

                item_bd['ProjectName'] = item_pd['ProjectName']

                item_bd['ProjectUUID'] = item_pd['ProjectUUID']

                item_bd['LssueDate'] = item_pd['LssueDate']

                item_bd['PresalePermitNumberUUID'] = item_pd[
                    'PresalePermitNumberUUID']

                item_bd['BuildingName'] = clean_rule2(
                    i.xpath('./td[1]/span/text()').extract_first())

                item_bd['PermitHouseCount'] = clean_rule2(
                    i.xpath('./td[2]/text()').extract_first())

                item_bd['BuildingPrice'] = clean_rule2(
                    i.xpath('./td[3]/text()').extract_first())

                item_bd['UnsoldAmount'] = clean_rule2(
                    i.xpath('./td[4]/text()').extract_first())

                item_bd['OnsoldAmount'] = clean_rule2(
                    i.xpath('./td[5]/text()').extract_first())

                item_bd['UnsoldArea'] = clean_rule2(
                    i.xpath('./td[7]/text()').extract_first())

                item_bd['OnsoldArea'] = clean_rule2(
                    i.xpath('./td[8]/text()').extract_first())

                item_bd['BuildingArea'] = clean_rule2(
                    i.xpath('./td[6]/text()').extract_first())

                item_bd['CancelCount'] = clean_rule2(
                    i.xpath('./td[11]/text()').extract_first())

                item_bd['BuildingUrl'] = 'https://61.143.53.130:4433/zhpubweb/' + \
                    i.xpath('./td[13]/font/a/@href').extract_first()

                item_bd['BuildingID'] = re.findall(
                    r'BuildNum\=(.+)', item_bd['BuildingUrl'])[0] if item_bd['BuildingUrl'] else ''

                item_bd['PresalePermitNumber'] = item_pd['PresalePermitNumber']

                item_bd['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, item_bd[
                                                     'ProjectName'] + item_bd['BuildingName'] + item_bd['PresalePermitNumber'])

                outcome_list.append(item_bd)

            url_pd = 'https://61.143.53.130:4433/zhpubweb/salemsg.aspx?readstate=ajax2&type=1&recnumgather={0}'.format(item_pd[
                                                                                                                       'RealEstateProjectID'])

            re_get = Request(url=url_pd, method='GET', headers=self.headers, meta={
                             'PageType': 'cd_url', "Item": dict(item_pd)}, dont_filter=True)

            outcome_list.append(re_get)

            return outcome_list

        else:

            return out_come

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class CertificateDetailMiddleware(object):

    headers = {"Referer": "https://61.143.53.130:4433/zhpubweb/projectQuery.aspx",
               "Host": "61.143.53.130:4433",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate,br",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               'Content-Type': 'application/x-www-form-urlencoded',
               'Origin': 'https://61.143.53.130:4433',
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
               }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(
            pagetype=['cd_url'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        if out_come == 'right' and pagetype == 'cd_url':

            item_cd = Certificate_Detail_Item()

            item_cd['ProjectName'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/projectname/text()').extract_first())

            item_cd['PresalePermitNumber'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/presalecert/text()').extract_first())

            item_cd['Developer'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/developer/text()').extract_first())

            item_cd['DeveloperPermitNumber'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/qualicert/text()').extract_first())

            item_cd['TotalBuidlingArea'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/area/text()').extract_first())

            item_cd['LandNumberAndUse'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/landcertinfo/text()').extract_first())

            item_cd['PresaleBuildingNo'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/buildinfo/text()').extract_first())

            item_cd['ProjectAddress'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/sitnumgather/text()').extract_first())

            item_cd['BuiltFloorCount'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/buildinfo2/text()').extract_first())

            item_cd['LivingCount'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/count1/text()').extract_first())

            item_cd['LivingArea'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/area1/text()').extract_first())

            item_cd['BusinessCount'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/count2/text()').extract_first())

            item_cd['BusinessArea'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/area2/text()').extract_first())

            item_cd['OtherCount'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/count3/text()').extract_first())

            item_cd['OtherArea'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/area3/text()').extract_first())

            item_cd['Bank'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/bank/text()').extract_first())

            item_cd['Bank_Account'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/bankacount/text()').extract_first())

            item_cd['ValidityDateStartDate'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/validstartdate/text()').extract_first())

            item_cd['ValidityDateClosingDate'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/validenddate/text()').extract_first())

            item_cd['LssueDate'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/passdate/text()').extract_first())

            item_cd['Remarks'] = clean_rule1(response.xpath(
                '/html/body/newdataset/table/recmemo/text()').extract_first())

            item_cd['ProjectUUID'] = response.meta['Item']['ProjectUUID']

            item_cd['PresalePermitNumberUUID'] = response.meta[
                'Item']['PresalePermitNumberUUID']

            item_cd['PresalePermitUrl'] = response.url

            outcome_list.append(item_cd)

            return outcome_list

        else:
            # print ('CertificateDetailMiddleware pass')

            # print(out_come)

            return out_come

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class HouseDetailMiddleware(object):

    headers = {"Referer": "https://61.143.53.130:4433/zhpubweb/projectQuery.aspx",
               "Host": "61.143.53.130:4433",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate,br",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Origin": "https://61.143.53.130:4433",
               'Content-Type': 'application/x-www-form-urlencoded',
               'Origin': 'https://61.143.53.130:4433',
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
               }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(
            pagetype=['hd_url'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        # print ('HouseDetailMiddleware')

        if out_come == 'right' and pagetype == 'hd_url':

            record_dict = response.meta['Record_Data']

            content_hd = response.xpath('//*[@id="GridViewProjectQuery"]/tr')

            checkdouble_set = response.meta.get('checkdouble_set') or set()

            cheack_page = response.xpath(
                '//*[@id="pageInfo"]/text()').extract_first()

            now_page = re.findall(r'第(.+?)页', cheack_page)[0]

            count_page = re.findall(r'共(.+?)页', cheack_page)[0]

            for i in content_hd[1:]:

                item_hd = House_Detail_Item()

                item_hd['ProjectName'] = record_dict['ProjectName']

                item_hd['ProjectUUID'] = record_dict['ProjectUUID']

                item_hd['BuildingName'] = record_dict['BuildingName']

                item_hd['BuildingUUID'] = record_dict['BuildingUUID']

                item_hd['PresalePermitNumber'] = record_dict[
                    'PresalePermitNumber']

                item_hd['PresalePermitNumberUUID'] = record_dict[
                    'PresalePermitNumberUUID']

                item_hd['SourceUrl'] = response.url

                item_hd['FloorName'] = clean_rule1(
                    i.xpath('./td[1]/text()').extract_first())

                item_hd['UnitName'] = clean_rule1(
                    i.xpath('./td[2]/text()').extract_first())

                item_hd['HouseName'] = clean_rule1(
                    i.xpath('./td[3]/text()').extract_first())

                item_hd['UnitShape'] = clean_rule1(
                    i.xpath('./td[4]/text()').extract_first())

                item_hd['HouseUseType'] = clean_rule1(
                    i.xpath('./td[5]/text()').extract_first())

                item_hd['Price'] = clean_rule1(
                    i.xpath('./td[6]/text()').extract_first())

                item_hd['BuildingArea'] = clean_rule1(
                    i.xpath('./td[7]/text()').extract_first())

                item_hd['InsideOfBuildingArea'] = clean_rule1(
                    i.xpath('./td[8]/text()').extract_first())

                item_hd['PublicArea'] = clean_rule1(
                    i.xpath('./td[9]/text()').extract_first())

                item_hd['HouseSaleState'] = clean_rule1(
                    i.xpath('./td[10]/text()').extract_first())

                item_hd['PresaleState'] = clean_rule1(
                    i.xpath('./td[11]/span/text()').extract_first())

                item_hd['HouseSaleStateLatest'] = ''

                item_hd['PresaleStateLatest'] = ''

                item_hd['PriceLatest'] = ''

                houseuuid_raw = item_hd['ProjectName'] + item_hd['PresalePermitNumber'] + item_hd[
                    'BuildingName'] + item_hd['UnitName'] + item_hd['HouseName'] + item_hd['BuildingArea']

                item_hd['HouseUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, houseuuid_raw)

                # 珠海城市存在相同户名等信息一样的户，发现存在重复的户用新的uuid规则
                if item_hd['HouseUUID'] in checkdouble_set:
                    # print (checkdouble_set)
                    # print ('double_state')
                    # print (item_hd['HouseUUID'])
                    houseuuid_raw = houseuuid_raw + now_page
                    item_hd['HouseUUID'] = uuid.uuid3(
                        uuid.NAMESPACE_DNS, houseuuid_raw)
                    outcome_list.append(item_hd)
                else:
                    # print ('first')
                    # print (item_hd['HouseUUID'])
                    checkdouble_set.add(item_hd['HouseUUID'])
                    outcome_list.append(item_hd)

            try:
                # print(now_page,count_page)
                if int(now_page) < int(count_page):
                    re_postbody = {"__EVENTTARGET": 'Button1',
                                   "__EVENTARGUMENT": "",
                                   "__VIEWSTATE": response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first(),
                                   "__EVENTVALIDATION": response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first(),
                                   "txtDeveloper": "",
                                   "newpage": int(now_page) + 1}
                    post_url = response.url
                    re_post = Request(url=post_url, method='POST', headers=self.headers, body=urlparse.urlencode(re_postbody), meta={
                                      'PageType': 'hd_url', 'Record_Data': record_dict, 'checkdouble_set': checkdouble_set}, dont_filter=True)
                    outcome_list.append(re_post)

            except Exception as e:

                print(e)

            return outcome_list

        else:
            # print ('HouseDetailMiddlewareover')

            return out_come


class MonitorMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(
            pagetype=['monitor'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        if (out_come == 'right') and (pagetype == 'monitor'):

            item = Monitor_Item()
            today = datetime.date.today()
            yestoday = (today - datetime.timedelta(days=1))
            table = response.xpath('//Table')
            cache_list = []

            for i in table[:-1]:
                cache_dict = {}
                c1 = i.xpath('./NAME/text()').extract_first()
                cache_dict['城市'] = c1
                cache_dict['住宅出售套数'] = clean_rule1(
                    i.xpath('./COUNT1/text()').extract_first())
                cache_dict['住宅出售均价'] = clean_rule1(
                    i.xpath('./PRICE1/text()').extract_first())
                cache_dict['商业出售套数'] = clean_rule1(
                    i.xpath('./COUNT2/text()').extract_first())
                cache_dict['商业出售均价'] = clean_rule1(
                    i.xpath('./PRICE2/text()').extract_first())
                cache_dict['办公出售套数'] = clean_rule1(
                    i.xpath('./COUNT3/text()').extract_first())
                cache_dict['办公出售均价'] = clean_rule1(
                    i.xpath('./PRICE3/text()').extract_first())
                cache_dict['其他出售套数'] = clean_rule1(
                    i.xpath('./COUNT4/text()').extract_first())
                cache_dict['其他出售均价'] = clean_rule1(
                    i.xpath('./PRICE4/text()').extract_first())

                cache_list.append(a)

            hj = table[-1]
            item['日期'] = str(yestoday.strftime('%Y-%m-%d'))
            item['来源链接'] = str(response.url)
            item['合计套数'] = hj.xpath('./COUNT1/text()').extract_first()
            item['合计均价'] = hj.xpath('./PRICE1/text()').extract_first()
            item['商业套数'] = hj.xpath('./COUNT2/text()').extract_first()
            item['商业均价'] = hj.xpath('./PRICE2/text()').extract_first()
            item['办公套数'] = hj.xpath('./COUNT3/text()').extract_first()
            item['办公均价'] = hj.xpath('./PRICE3/text()').extract_first()
            item['其他套数'] = hj.xpath('./COUNT4/text()').extract_first()
            item['其他均价'] = hj.xpath('./PRICE4/text()').extract_first()
            item['当天出售楼栋'] = cache_list

            outcome_list.append(item)

            return outcome_list

        else:

            return out_come

# coding = utf-8
# -*- coding: utf-8 -*-
import copy
import json
import re
import time
import uuid

from HouseCrawler.Items.ItemsFS import *
from HouseNew.models import *
from scrapy import Request

clean_rule1 = lambda x: x.strip().replace('\r', "") if x else ''
clean_rule2 = lambda x: x.strip().replace('\n', ";").replace('\r', "").replace('\t', '') if x else ''


def cheack_response(pagetype, response, result):
    if (response.meta.get('PageType') in pagetype) and (200 <= response.status < 303):

        out_come = 'right' if result else []

    else:
        out_come = result if result else []

    return out_come


class ProjectListMiddleware(object):
    headers = {"Referer": "http://fsfc.fsjw.gov.cn/",
               "Host": "fsfc.fsjw.gov.cn",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
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

        out_come = cheack_response(pagetype=['pl_url'], response=response, result=result)

        if out_come == 'right':

            outcome_list, pagetype, recorddata_dict = [], response.meta['PageType'], response.meta['Record_Data']

            print('ProjectGetFidMiddleware')

            crawler_type = recorddata_dict['crawler_type']

            content = response.xpath('//*[@id="content"]/div[2]/div[1]/dl')

            for i in content:
                item_pd = Project_Detail_Item()

                item_pd['RealEstateProjectID'] = i.xpath('./dd/h3/a/@value').extract_first()

                item_pd['ProjectUrl'] = 'http://fsfc.fsjw.gov.cn/hpms_project/roomView.jhtml?id={0}'.format(
                    item_pd['RealEstateProjectID'])

                item_pd['HouseSoldAmount'] = i.xpath('./dd/p[4]/em[1]/text()').extract_first()

                item_pd['HouseUnsoldAmount'] = i.xpath('./dd/p[4]/em[2]/text()').extract_first()

                item_pd['SourceUrl'] = response.url

                re_get = Request(url=item_pd['ProjectUrl'], method='GET', meta={'PageType': 'pd_url', "Item": item_pd},
                                 dont_filter=True)

                outcome_list.append(re_get)

            if crawler_type == 'ini':

                # print (recorddata_dict['pages_num'])

                record_number = response.xpath(
                    '//*[@id="content"]/div[2]/div[1]/div[2]/form/span[1]/text()').extract_first()

                try:
                    record_number = int(re.findall(r'(\d.+?)\D', record_number)[0])

                except Exception as e:

                    record_number = '2716'

                if recorddata_dict['pages_num'] < int(record_number / 10) + 1:
                    recorddata_dict['pages_num'] += 1

                    url_next = "http://fsfc.fsjw.gov.cn/search/index.do?sw=&dn=&hx=&lx=&mj=&jg=&ys=0&od=-SORT;-STIME;-LASTMODIFYTIME;RELEVANCE&p={0}".format(
                        recorddata_dict['pages_num'])

                    re_get = Request(url=url_next, method='GET', headers=self.headers,
                                     meta={'PageType': 'pl_url', "Record_Data": recorddata_dict}, dont_filter=True)

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


class ProjectDetailMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    headers = {"Referer": "http://fsfc.fsjw.gov.cn/",
               "Host": "fsfc.fsjw.gov.cn",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
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
        print('ProjectListMiddleware')
        out_come = cheack_response(pagetype=['pd_url'], response=response, result=result)
        outcome_list = []
        pagetype = response.meta['PageType']
        if (out_come == 'right') and (pagetype == 'pd_url'):
            item_pd = response.meta['Item']
            item_pd['ProjectName'] = clean_rule1(response.xpath(
                '//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[1]/td/strong/span/text()').extract_first())
            item_pd['ProjectAddress'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[2]/td/span/text()').extract_first())
            item_pd['DistrictName'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[3]/td[2]/text()').extract_first())
            item_pd['Developer'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[3]/td[1]/span/@title').extract_first())
            item_pd['ManagementCompany'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[4]/td[1]/span/text()').extract_first())
            item_pd['ManagementFees'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[4]/td[2]/span/text()').extract_first())
            Project_raw = item_pd['ProjectName'] + item_pd["RealEstateProjectID"]
            item_pd['ProjectUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, Project_raw)
            item_pd['TotalBuidlingArea'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[5]/td[1]/text()').extract_first())
            item_pd['FloorAreaRatio'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[5]/td[2]/span/text()').extract_first())
            item_pd['DeveloperPermitNumber'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[6]/td[1]/text()').extract_first())
            item_pd['DeveloperLevel'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[6]/td[2]/text()').extract_first())
            item_pd['AveragePrice'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[7]/td[1]/em/text()').extract_first())
            item_pd['SaleTelphoneNumber'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div[1]/div[2]/table/tr[7]/td[2]/span/text()').extract_first())
            item = copy.deepcopy(item_pd)
            outcome_list.append(item)
            cretificate_url = 'http://fsfc.fsjw.gov.cn/hpms_project/ysxkz.jhtml?id={0}'.format(
                item_pd['RealEstateProjectID'])
            re_get = Request(url=cretificate_url, method='GET', meta={'PageType': 'cd_url', "Item": item},
                             dont_filter=True)
            outcome_list.append(re_get)
            building_content = response.xpath('//*[@id="content"]/div[2]/div[1]/td')

            for i in building_content:
                item_bd = Building_Detail_Item()
                item_bd['ProjectName'] = item_pd['ProjectName']
                item_bd['ProjectUUID'] = str(item_pd['ProjectUUID'])
                item_bd['RealEstateProjectID'] = item_pd['RealEstateProjectID']
                item_bd['RegionName'] = item_pd['DistrictName']
                item_bd['BuildingName'] = clean_rule1(i.xpath('./a/text()').extract_first())
                item_bd['BuildingID'] = clean_rule1(i.xpath('./a/@id').extract_first())
                item_bd['BuildingUrl'] = 'http://fsfc.fsjw.gov.cn/hpms_project/' + clean_rule1(
                    i.xpath('./a/@href').extract_first())
                BuildingUUID_raw = (item_pd['ProjectName'] + item_bd['BuildingName'] + item_bd['BuildingID'])
                item_bd['BuildingUUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, BuildingUUID_raw))
                item_bd['SourceUrl'] = response.url
                outcome_list.append(item_bd)

            return outcome_list
        else:
            return out_come

    def process_spider_exception(self, response, exception, spider):
        return


class BuildingDetailMiddleware(object):
    headers = {"Referer": "http://fsfc.fsjw.gov.cn/",
               "Host": "fsfc.fsjw.gov.cn",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
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

        out_come = cheack_response(pagetype=['bd_url'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        if out_come == 'right':

            item_raw = response.meta['Item']

            item_bd = Building_Detail_Item()

            response_json = json.loads(response.text)

            item_bd['UnsoldAmount'] = str(response_json['wsts'])

            item_bd['OnsoldAmount'] = str(response_json['ysts'])

            item_bd['Floors'] = str(response_json['zcs'])

            item_bd['ProjectName'] = item_raw['ProjectName']

            item_bd['ProjectUUID'] = item_raw['ProjectUUID']

            item_bd['RealEstateProjectID'] = item_raw['RealEstateProjectID']

            item_bd['RegionName'] = item_raw['RegionName']

            item_bd['BuildingName'] = item_raw['BuildingName']

            item_bd['BuildingID'] = item_raw['BuildingID']

            item_bd['BuildingUrl'] = item_raw['BuildingUrl']

            item_bd['BuildingUUID'] = item_raw['BuildingUUID']

            item_bd['SourceUrl'] = item_raw['SourceUrl']

            outcome_list.append(item_bd)

            return outcome_list

        else:
            # print ('BuildingDetailMiddlewareover')
            return out_come

    def process_spider_exception(self, response, exception, spider):

        return


class CertificateDetailMiddleware(object):
    headers = {
        "Host": "fsfc.fsjw.gov.cn",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
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

        out_come = cheack_response(pagetype=['cd_url', 'cd_url2'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        if (out_come == 'right') and (pagetype == 'cd_url'):

            outcome_list, item_cache = [], response.meta['Item']

            certificate_content = response.xpath('//*[@id="selsect"]/option')

            for i in certificate_content:
                item_cd = Certificate_Detail_Item()

                item_cd['ProjectName'] = item_cache['ProjectName']

                item_cd['ProjectUUID'] = item_cache['ProjectUUID']

                item_cd['RealEstateProjectID'] = item_cache['RealEstateProjectID']

                item_cd['PresalePermitNumber'] = clean_rule1(i.xpath('./text()').extract_first())

                item_cd['PresalePermitNumberID'] = clean_rule1(i.xpath('./@value').extract_first())

                item_cd['PresalePermitNumberUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                item_cd['ProjectName'] + item_cd['PresalePermitNumber'])

                item_cd['PresalePermitUrl'] = "http://fsfc.fsjw.gov.cn/hpms_project/ysxkzxx.jhtml?xkzh={0}".format(
                    item_cd['PresalePermitNumberID'])

                re_get = Request(url=item_cd['PresalePermitUrl'], method='GET',
                                 meta={'PageType': 'cd_url2', "Item": item_cd}, dont_filter=True)

                outcome_list.append(re_get)

            return outcome_list

        elif (out_come == 'right') and (response.meta['PageType'] == 'cd_url2'):

            item_cd = response.meta['Item']

            response_json = json.loads(response.text)

            # print (response_json)

            item_cd['PresaleHouseCount'] = str(response_json['yszts'])

            item_cd['PresaleTotalBuidlingArea'] = str(response_json['yszmj'])

            item_cd['LssuingAuthority'] = str(response_json['fzjg'])

            item_cd['Bank'] = str(response_json['yszjkhyh'])

            item_cd['Bank_Account'] = str(response_json['yszjzh'])

            item_cd['LivingArea'] = str(response_json['zzmj'])

            item_cd['LivingCount'] = str(response_json['zzts'])

            item_cd['BusinessArea'] = str(response_json['symj'])

            item_cd['BusinessCount'] = str(response_json['syts'])

            item_cd['OtherArea'] = str(response_json['qtmj'])

            item_cd['OtherCount'] = str(response_json['qtts'])

            item_cd['PresaleBuildingNo'] = str(response_json['jdZh1'])

            item_cd['SourceUrl'] = response.url

            item_cd['ValidityDateStartDate'] = time.strftime("%Y-%m-%d",
                                                             time.localtime(response_json['yxqx1'] / 1000)) if \
                response_json['yxqx1'] else ''

            item_cd['ValidityDateClosingDate'] = time.strftime("%Y-%m-%d",
                                                               time.localtime(response_json['yxqx2'] / 1000)) if \
                response_json['yxqx2'] else ''

            item_cd['LssueDate'] = time.strftime("%Y-%m-%d", time.localtime(response_json['fzrq'] / 1000)) if \
                response_json['fzrq'] else ''

            item2 = copy.deepcopy(item_cd)

            outcome_list.append(item2)

            return outcome_list

        else:
            print('CertificateDetailMiddleware pass')

            # print(out_come)

            return out_come

    def process_spider_exception(self, response, exception, spider):
        return


class HouseDetailMiddleware(object):
    headers = {
        "Host": "fsfc.fsjw.gov.cn",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(pagetype=['hd_url', 'hd_url2'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        print('HouseDetailMiddleware')

        if (out_come == 'right') and (pagetype == 'hd_url'):

            record_dict = response.meta['Record_Data']

            item_hd = House_Detail_Item()

            content = json.loads(response.text)

            item_hd['ProjectName'] = record_dict['ProjectName']

            item_hd['ProjectUUID'] = record_dict['ProjectUUID']

            item_hd['RegionName'] = record_dict['RegionName']

            item_hd['BuildingName'] = record_dict['BuildingName']

            item_hd['BuildingUUID'] = record_dict['BuildingUUID']

            item_hd['SourceUrl'] = response.url

            for i in content:

                item_hd['HouseName'] = str(i['roomno'])

                item_hd['UnitName'] = str(i['unitname'])

                item_hd['HouseUseType'] = str(i['ghyt'])

                item_hd['HouseID'] = str(i['fwcode'])

                houseuuid_raw = item_hd['ProjectName'] + item_hd['BuildingName'] + item_hd['UnitName'] + item_hd[
                    'HouseName'] + str(item_hd['HouseID'])

                item_hd['HouseUUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, houseuuid_raw))

                item_hd['HouseUrl'] = 'http://fsfc.fsjw.gov.cn/hpms_project/roomview.jhtml?id={0}'.format(
                    item_hd['HouseID'])

                item_hd['FloorName'] = str(i['floorname'])

                item_hd['HouseSaleState'] = str(i['zt'])

                item_hd['ComplateTag'] = 0

                count_times = re.findall(item_hd['HouseID'], response.text)

                if count_times.__len__() > 1:

                    print(item_hd['HouseName'])

                    print(item_hd['HouseID'])

                    re_get = Request(url=item_hd['HouseUrl'], method='GET',
                                     meta={'PageType': 'hd_url2', "Item": copy.deepcopy(item_hd),
                                           'Tag': 'double_status'})

                    outcome_list.append(re_get)

                else:

                    item = copy.deepcopy(item_hd)

                    outcome_list.append(item)

            return outcome_list

        elif (out_come == 'right') and (pagetype == 'hd_url2'):

            item_hd = response.meta['Item']

            item_hd['HouseNature'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[4]/td[2]/text()').extract_first())

            item_hd['HouseType'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[3]/td[4]/text()').extract_first())

            item_hd['BalconyType'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[5]/td[4]/text()').extract_first())

            item_hd['ForecastBuildingArea'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[6]/td[2]/text()').extract_first())

            item_hd['ForecastInsideOfBuildingArea'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[7]/td[2]/text()').extract_first())

            item_hd['ForecastPublicArea'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[8]/td[2]/text()').extract_first())

            item_hd['MeasuredBuildingArea'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[6]/td[4]/text()').extract_first())

            item_hd['MeasuredInsideOfBuildingArea'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[7]/td[4]/text()').extract_first())

            item_hd['MeasuredSharedPublicArea'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[8]/td[4]/text()').extract_first())

            item_hd['IsMortgage'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[9]/td[2]/text()').extract_first())

            item_hd['IsAttachment'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[9]/td[4]/text()').extract_first())

            item_hd['Adress'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[11]/td[2]/text()').extract_first())

            item_hd['TotalPrice'] = clean_rule1(
                response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[10]/td[4]/text()').extract_first())

            item_hd['ComplateTag'] = 1

            if response.meta.get('Tag') == 'double_status':
                print('double_status')

                item_hd['HouseSaleState'] = clean_rule1(
                    response.xpath('//*[@id="content"]/div[2]/div/div/table[1]/tr[10]/td[2]/text()').extract_first())

            outcome_list.append(item_hd)

            return outcome_list

        else:
            return out_come


class MonitorMiddleware(object):
    headers = {
        "Host": "fsfc.fsjw.gov.cn",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(pagetype=['monitor'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        if (out_come == 'right') and (pagetype == 'monitor'):

            item = Monitor_Item()

            item['riqi'] = time.strftime("%Y-%m-%d", time.localtime())
            item['quanshi_zhuzhai_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-color"]/td[2]/span/@title').extract_first())
            item['quanshi_zhuzhai_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-color"]/td[3]/span/@title').extract_first())
            item['quanshi_shangye_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-color"]/td[4]/span/@title').extract_first())
            item['quanshi_shangye_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-color"]/td[5]/span/@title').extract_first())
            item['quanshi_qita_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-color"]/td[6]/span/@title').extract_first())
            item['quanshi_qita_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-color"]/td[7]/span/@title').extract_first())

            item['chancheng_zhuzhai_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][1]/td[2]/span/@title').extract_first())
            item['chancheng_zhuzhai_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][1]/td[3]/span/@title').extract_first())
            item['chancheng_shangye_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][1]/td[4]/span/@title').extract_first())
            item['chancheng_shangye_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][1]/td[5]/span/@title').extract_first())
            item['chancheng_qita_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][1]/td[6]/span/@title').extract_first())
            item['chancheng_qita_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][1]/td[7]/span/@title').extract_first())

            item['nanhan_zhuzhai_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][2]/td[2]/span/@title').extract_first())
            item['nanhan_zhuzhai_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][2]/td[3]/span/@title').extract_first())
            item['nanhan_shangye_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][2]/td[4]/span/@title').extract_first())
            item['nanhan_shangye_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][2]/td[5]/span/@title').extract_first())
            item['nanhan_qita_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][2]/td[6]/span/@title').extract_first())
            item['nanhan_qita_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][2]/td[7]/span/@title').extract_first())

            item['shunde_zhuzhai_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][3]/td[2]/span/@title').extract_first())
            item['shunde_zhuzhai_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][3]/td[3]/span/@title').extract_first())
            item['shunde_shangye_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][3]/td[4]/span/@title').extract_first())
            item['shunde_shangye_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][3]/td[5]/span/@title').extract_first())
            item['shunde_qita_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][3]/td[6]/span/@title').extract_first())
            item['shunde_qita_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][3]/td[7]/span/@title').extract_first())

            item['gaoming_zhuzhai_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][4]/td[2]/span/@title').extract_first())
            item['gaoming_zhuzhai_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][4]/td[3]/span/@title').extract_first())
            item['gaoming_shangye_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][4]/td[4]/span/@title').extract_first())
            item['gaoming_shangye_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][4]/td[5]/span/@title').extract_first())
            item['gaoming_qita_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][4]/td[6]/span/@title').extract_first())
            item['gaoming_qita_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][4]/td[7]/span/@title').extract_first())

            item['sanshui_zhuzhai_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][5]/td[2]/span/@title').extract_first())
            item['sanshui_zhuzhai_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][5]/td[3]/span/@title').extract_first())
            item['sanshui_shangye_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][5]/td[4]/span/@title').extract_first())
            item['sanshui_shangye_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][5]/td[5]/span/@title').extract_first())
            item['sanshui_qita_taoshu'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][5]/td[6]/span/@title').extract_first())
            item['sanshui_qita_mianji'] = clean_rule1(
                response.xpath('//tr[@class="tr-bg"][5]/td[7]/span/@title').extract_first())

            outcome_list.append(item)

            return outcome_list


        else:
            # print ('HouseDetailMiddlewareover')

            return out_come

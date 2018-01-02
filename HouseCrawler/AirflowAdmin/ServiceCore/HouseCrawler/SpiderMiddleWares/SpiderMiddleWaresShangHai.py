#!/usr/python3
# -*- coding: utf-8 -*-
import sys
import logging
import uuid
import re
import copy
import random
from HouseCrawler.Items.ItemsShangHai import *
from HouseNew.models import *
from scrapy import Request
from scrapy import Selector


if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
def check_data_str(string):
    result_data = ''
    if string:
        fix_data = string.strip().replace('\r', '').replace('\n', '')\
        .replace('\t', '').replace('\\', '').replace('n', '').replace('t', '')\
        .replace(' ', '').replace(" ","")
        if fix_data !='' and '*' not in fix_data:
            result_data = fix_data
    return result_data
'''
获取所有项目链接信息
'''
class GetProjectBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': 'www.fangdi.com.cn',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                }



    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://www.fangdi.com.cn/'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('GetProjectBase'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'GetProjectBase':
            result1 = response.xpath('//*[@id="Table7"]/tr/td[5]').extract()
            result2 = response.xpath('//*[@id="Table7"]/tr/td[4]').extract()
            if result1:
                result1 = result1[0].replace('\r', ''). \
                    replace('\n', '').replace('\t', ''). \
                    replace(' ', '').replace(u' ', '')
                if 'optionselectedvalue' in result1:
                    project_links = re.findall(r'value="/(.*?)"', result1)
                    for project_link in project_links:
                        project_link = self.shprojectmain_url + project_link.replace("amp;", "")
                        result.append(Request(url=project_link,
                                              meta={
                                                  'PageType': 'ProjectBase'
                                              }))

            elif result2:
                result2 = result2[0].replace('\r', ''). \
                    replace('\n', '').replace('\t', ''). \
                    replace(' ', '').replace(u' ', '')
                if 'optionselectedvalue' in result2:
                    project_links = re.findall(r'value="/(.*?)"', result2)
                    for project_link in project_links:
                        logging.debug(project_link)
                        project_link = self.shprojectmain_url + project_link.replace("amp;", "")
                        result.append(Request(url=project_link,
                                              meta={
                                                  'PageType': 'ProjectBase'
                                              }))

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


'''
获取项目页面信息
'''
class ProjectBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': 'www.fangdi.com.cn',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                }



    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://www.fangdi.com.cn/'
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectBase','SubProject'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'ProjectBase':
            #/html/body/center/table[6]/tbody/tr[2]/td[2]/a
            results = Selector(response).xpath("/html/body/center/table[6]/tr")
            for get_result in results[1:]:
                shprojectitem = ProjectBaseItem()
                shprojectitem['project_sts'] = get_result.xpath('./td[1]/text()').extract_first()
                shprojectitem['project_addr'] = get_result.xpath('./td[3]/text()').extract_first()
                shprojectitem['project_house_num'] = get_result.xpath('./td[4]/text()').extract_first()
                shprojectitem['project_house_area'] = get_result.xpath('./td[5]/text()').extract_first()
                prdetailhref = get_result.xpath('./td[2]/a/@href').extract_first()
                # if 'middle' in get_result:
                #     get_result = get_result.replace('\r', ''). \
                #         replace('\n', '').replace('\t', ''). \
                #         replace(' ', '').replace(u' ', '')
                #
                #     #/html/body/center/table[5]/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]
                #     myItems = re.findall('tyle="padding:3">(.*?)</td>', get_result, re.S)
                #
                #     shprojectitem['project_sts'] = myItems[0]
                #     shprojectitem['project_addr'] = myItems[2]
                #     shprojectitem['project_house_num'] = myItems[3]
                #     shprojectitem['project_house_area'] = myItems[4]
                #     prdetailhref = re.search('href="(.*?)"', myItems[1], re.S)
                if prdetailhref:
                        new_url = self.shprojectmain_url + prdetailhref
                        req = Request(url=new_url,
                                      meta={
                                          'PageType': 'SubProject',
                                          'item': shprojectitem
                                      },
                                      dont_filter=True)
                        result.append(req)
        if response.meta.get('PageType') == 'SubProject':
            print('SubProject')
            SubProject_base = response.meta.get('item')
            shprojectitem = copy.deepcopy(SubProject_base)
            # /html/body/center/table[5]/tr/td/table[2]/tr/td[2]/table/tr[2]/td/table/tr[1]/td[2]
            #/html/body/center/table[5]/tr/td/table/tr/table/tr[1]/td[2]/table/tr[2]/td/table/tr[1]
            shprojectitem['project_name'] = check_data_str(Selector(response).xpath(
                '/html/body/center/table[5]/tr/td/table/tr/table/tr[1]/td[2]/table/tr[2]/td/table/tr[1]/td[2]/text()').extract_first())
            # /html/body/center/table[5]/tbody/tr/td/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[4]
            shprojectitem['project_county'] = check_data_str(Selector(response).xpath(
                '/html/body/center/table[5]/tr/td/table/tr/table/tr[1]/td[2]/table/tr[2]/td/table/tr[1]/td[4]/text()').extract_first())
            shprojectitem['project_blank'] = check_data_str(Selector(response).xpath(
                '/html/body/center/table[5]/tr/td/table/tr/table/tr[1]/td[2]/table/tr[2]/td/table/tr[2]/td[4]/text()').extract_first())
            project_no = uuid.uuid3(uuid.NAMESPACE_DNS, shprojectitem['project_name']).hex
            shprojectitem['project_no'] = str(project_no)
            shprojectitem['project_com_name'] = check_data_str(Selector(response).xpath(
                '/html/body/center/table[5]/tr/td/table/tr/table/tr[1]/td[2]/table/tr[2]/td/table/tr[3]/td[2]/a/text()').extract_first())
            shprojectitem['project_price'] = check_data_str(
                Selector(response).xpath('//*[@id="div2"]/table/tr[1]/td[3]/div/text()').extract_first())
            shprojectitem['project_price_house'] = check_data_str(
                Selector(response).xpath('//*[@id="div2"]/table/tr[1]/td[7]/div/text()').extract_first())
            shprojectitem['project_price_back'] = check_data_str(
                Selector(response).xpath('//*[@id="div2"]/table/tr[3]/td[3]/div/text()').extract_first())
            shprojectitem['project_price_house_back'] = check_data_str(
                Selector(response).xpath('//*[@id="div2"]/table/tr[3]/td[7]/div/text()').extract_first())

            project_image_link = Selector(response).xpath(
                '//*[@id="div1"]/table/tr/td/img/@src').extract_first()
            shprojectitem['project_detail_link'] = self.shprojectmain_url + project_image_link

            #//*[@id="SUList"]
            project_sub_link = Selector(response).xpath(
                '//*[@id="SUList"]/@src').extract_first()
            openinguniturl = self.shprojectmain_url + project_sub_link
            result.append(shprojectitem)
            result.append(Request(url=openinguniturl,
                                  meta={
                                      'PageType': 'openingunit',
                                      'project_no': project_no,
                                      'project_name':shprojectitem['project_name']
                                  }
                                  ))

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


'''
处理开盘单元页面
'''
class OpenningunitBaseHandleMiddleware(object):

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': 'www.fangdi.com.cn',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                }



    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://www.fangdi.com.cn/'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('openingunit'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'openingunit':
            project_no = response.meta['project_no']
            project_name = response.meta['project_name']
            responsetext = response.body.decode('gbk')

            openingunitdetails = re.findall(r';">(.*?)/font>', responsetext, re.S)
            for openingunitdetail in openingunitdetails:
                openingunitdetail = openingunitdetail.replace('\r', ''). \
                    replace('\n', '').replace('\t', ''). \
                    replace(' ', '').replace(' ', '')
                openingunititem = OpeningunitItem()
                openingunititem['project_no'] = str(project_no)
                openingunititem['project_name'] = str(project_name)
                item_details = re.findall(r'<tdheight="19">(.*?)</td>', openingunitdetail)
                opening_unit_no = item_details[0]
                openingunititem['opening_unit_no'] = opening_unit_no
                building_url = self.shprojectmain_url + 'building.asp' + re.search(
                    'building.asp(.*?)"', openingunitdetail, re.S).group(1)
                openingunititem['opening_building_detail_link'] = str(building_url)
                openingunititem['opening_unit_licence'] = re.search(
                    'bold">(.*?)</span>', item_details[1], re.S).group(1)
                openingunititem['opening_unit_opendate'] = item_details[2]
                openingunititem['opening_unit_num'] = item_details[3]
                openingunititem['opening_unit_housenum'] = item_details[4]
                openingunititem['opening_unit_area'] = item_details[5].replace("<sup>", ""). \
                    replace("</sup>", "").replace("<SUP>", "").replace("</SUP>", "")
                openingunititem['opening_unit_housearea'] = item_details[6].replace("<sup>", ""). \
                    replace("</sup>", "").replace("<SUP>", "").replace("</SUP>", "")
                if 'green' in openingunitdetail:
                    openingunititem['opening_unit_sts'] = u"在售"
                    result.append(Request(url=building_url,
                                          meta={
                                              'PageType': 'building',
                                              'project_no': str(project_no),
                                              'opening_unit_no': opening_unit_no,
                                              'project_name':project_name
                                          }))

                else:
                    openingunititem['opening_unit_sts'] = u"售完"
                result.append(openingunititem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


'''
处理楼栋页面
'''
class BuildingBaseHandleMiddleware(object):

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': 'www.fangdi.com.cn',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                }



    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://www.fangdi.com.cn/'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('building'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'building':
                project_no = response.meta.get('project_no')
                project_name = response.meta.get('project_name')
                opening_unit_no = response.meta.get('opening_unit_no')

                responsetext = response.body.decode('gbk')
                # responsetext = response.body_as_unicode()
                openingunitpagedetails = re.findall(r'class="indextabletxt">(.*?)</tr>', responsetext, re.S)
                for openingunitpagedetail in openingunitpagedetails:
                    openingunitpagedetail = openingunitpagedetail.replace('\r', ''). \
                        replace('\n', '').replace('\t', ''). \
                        replace(' ', '').replace(u' ', '')
                    buildingitemdetails = re.findall(r'tdalign="center"style="padding:3">(.*?)</td>',
                                                     openingunitpagedetail)
                    buildingitem = BuildingItem()
                    buildingitem['project_no'] = project_no
                    buildingitem['project_name'] = project_name
                    buildingitem['opening_unit_no'] = opening_unit_no
                    building_name = re.search(r'TARGET="_BLANK">(.*?)</a>', buildingitemdetails[0], re.S).group(1)
                    buildingitem['building_name'] = building_name
                    building_no = uuid.uuid3(uuid.NAMESPACE_DNS, str(building_name)).hex
                    buildingitem['building_no'] = str(building_no)
                    buildingitem['building_price'] = buildingitemdetails[1]
                    buildingitem['building_fluctuation'] = buildingitemdetails[2]
                    if buildingitemdetails[3].isdigit():
                        buildingitem['building_num'] = buildingitemdetails[3]
                    else:
                        buildingitem['building_num'] = '0'
                    buildingitem['building_area'] = buildingitemdetails[4]
                    building_detail_page_url = self.shprojectmain_url + 'House.asp' + re.search(
                        'House.asp(.*?)"', buildingitemdetails[0], re.S).group(1)
                    buildingitem['building_url'] = building_detail_page_url
                    if 'green' in buildingitemdetails[5]:
                        buildingitem['building_sts'] = u"在售"

                    else:
                        buildingitem['building_sts'] = u"售完"
                    result.append(buildingitem)
        return result
    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


'''
处理每栋楼中房屋页面
'''
class HouseBaseHandleMiddleware(object):

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': 'www.fangdi.com.cn',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                }



    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://www.fangdi.com.cn/'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseBase','HouseInfo'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'HouseBase':
            project_no = response.meta.get('project_no')
            project_name = response.meta.get('project_name')
            opening_unit_no = response.meta.get('opening_unit_no')
            building_no = response.meta.get('building_no')

            building_detail_results = response.xpath('//*[@id="Table1"]/tr/td/table[2]/tr').extract()
            house_sts_classify = {'#FFFF00': '已签',
                                  '#FF0000': '已登记',
                                  '#00C200': '可售',
                                  '#FF00FF': '已付定金',
                                  '#FFFFFF': '未纳入网上销售',
                                  'FFFFFF': '未纳入网上销售'
                                  }
            #
            house_type_classify = {
                'circular': u'动迁房',
                'pentagram': u'配套商品房',
                'trangle': u'动迁安置房'
            }
            self.recnum = 0
            for building_detail_result in building_detail_results:
                building_detail_result = building_detail_result.replace('\r', ''). \
                    replace('\n', '').replace('\t', ''). \
                    replace(' ', '').replace(u' ', '')
                real_floor = re.search('<u>(.*?)</u>', building_detail_result, re.S).group(1)
                house_details = re.findall(r'<tdbgcolor(.*?)</td>', building_detail_result)
                recordhouse = []
                for house_detail in house_details:
                    house_detail = house_detail.replace("△", "trangle"). \
                        replace("●", "circular").replace("☆", "pentagram")
                    houseitem = HouseItem()
                    houseitem['project_no'] = project_no
                    houseitem['project_name'] = project_name
                    houseitem['opening_unit_no'] = opening_unit_no
                    houseitem['building_no'] = building_no
                    houseitem['house_floor'] = real_floor
                    house_type = re.search('="(.*?)"align', house_detail, re.S).group(1)
                    if house_type:
                        house_sts = house_sts_classify[house_type]
                    else:
                        house_sts = u'属于其它开盘单元'
                    houseitem['house_sts'] = house_sts
                    self.recnum = self.recnum + 1
                    house_no = uuid.uuid3(uuid.NAMESPACE_DNS, str(self.recnum)).hex
                    while house_no in recordhouse:
                        house_no = house_no + '1'
                    recordhouse.append(house_no)
                    houseitem['house_no'] = opening_unit_no + building_no + str(house_no) + real_floor
                    if u'circular' in house_detail:
                        houseitem['house_class'] = house_type_classify['circular']
                    elif u'pentagram' in house_detail:
                        houseitem['house_class'] = house_type_classify['pentagram']
                    elif u'trangle' in house_detail:
                        houseitem['house_class'] = house_type_classify['trangle']
                    else:
                        houseitem['house_class'] = u'普通'
                    house_area_pr_yc = re.search(u'预测面积：(.*?)/', house_detail, re.S)
                    if house_area_pr_yc:
                        if len(house_area_pr_yc.group(1)) < 20:
                            houseitem['house_area_pr_yc'] = house_area_pr_yc.group(1)
                        else:
                            house_area_pr_yc = re.search(u'预测面积：(.*?)平方米', house_detail, re.S)
                            houseitem['house_area_pr_yc'] = house_area_pr_yc.group(1)
                    house_area_real_yc = re.search(u'实测面积:(.*?)平方米', house_detail, re.S)
                    if house_area_real_yc:
                        houseitem['house_area_real_yc'] = house_area_real_yc.group(1)
                    if 'href' in house_detail:
                        house_num = re.search(r'"black">(.*?)</font>', house_detail, re.S)

                        if house_num:
                            house_num = str(house_num.group(1)).replace("（", "(").replace("）", ")")
                            houseitem['house_num'] = house_num
                    else:
                        house_num = re.search(r'平方米">(.*?)<br>', house_detail, re.S)
                        if house_num:
                            house_num = str(house_num.group(1)).replace("（", "(").replace("）", ")")
                            houseitem['house_num'] = house_num
                    if house_sts == '可售':
                        house_detail_detail = re.search(r'housedetail.asp(.*?)"', house_detail, re.S)
                        if house_detail_detail:
                            house_detail_page_url = self.shprojectmain_url + 'housedetail.asp' + house_detail_detail.group(
                                1).replace("amp;", "")
                            result.append(Request(url=house_detail_page_url,
                                                  meta={
                                                      'PageType': 'HouseInfo',
                                                      'item': houseitem},
                                                  dont_filter=True))
                    else:
                        result.append(houseitem)
        if response.meta.get('PageType') == 'HouseInfo':
            houseBaseitem = response.meta.get('item')
            newhouseitem = copy.deepcopy(houseBaseitem)
            newhouseitem['house_use_type'] = check_data_str(
                Selector(response).xpath('//*[@id="Table1"]/tr/td/table/tbody/tr[4]/td[2]/text()').extract_first())

            newhouseitem['house_layout'] = check_data_str(
                Selector(response).xpath('//*[@id="Table1"]/tr/td/table/tbody/tr[5]/td[2]/text()').extract_first())

            newhouseitem['house_area_pr_tn'] = check_data_str(
                Selector(response).xpath('//*[@id="Table1"]/tr/td/table/tbody/tr[7]/td[2]/text()').extract_first())

            newhouseitem['house_area_pr_ft'] = check_data_str(
                Selector(response).xpath('//*[@id="Table1"]/tr/td/table/tbody/tr[8]/td[2]/text()').extract_first())

            newhouseitem['house_area_pr_dx'] = check_data_str(
                Selector(response).xpath('//*[@id="Table1"]/tr/td/table/tbody/tr[9]/td[2]/text()').extract_first())

            newhouseitem['house_area_real_tn'] = check_data_str(
                Selector(response).xpath('//*[@id="Table1"]/tr/td/table/tbody/tr[11]/td[2]/text()').extract_first())

            newhouseitem['house_area_real_ft'] = check_data_str(
                Selector(response).xpath('//*[@id="Table1"]/tr/td/table/tbody/tr[12]/td[2]/text()').extract_first())

            newhouseitem['house_area_real_dx'] = check_data_str(
                Selector(response).xpath('//*[@id="Table1"]/tr/td/table/tbody/tr[13]/td[2]/text()').extract_first())

            result.append(newhouseitem)
        return result
    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return

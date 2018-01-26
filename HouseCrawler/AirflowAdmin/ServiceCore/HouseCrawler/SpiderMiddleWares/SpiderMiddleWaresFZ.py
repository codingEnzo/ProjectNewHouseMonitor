#!/usr/python3
# -*- coding: utf-8 -*-
import sys
import uuid
import re
import copy
import json
import random
import redis
from scrapy import Request
from scrapy import Selector

from HouseNew.models import *
from HouseCrawler.Items.ItemsFZ import *
if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
'''
获取所有项目链接信息
'''
# contextflag = False
contextflag = True
'''
获取项目列表页面
'''


class GetProjectPageBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': '222.77.178.63:7002',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               }

    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://222.77.178.63:7002/'
        self.r = redis.Redis(host='10.30.1.18', port=6379)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('GetProjectBase'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'GetProjectBase':
            pageresults = response.xpath(
                "/html/body/table[1]/tr[2]/td/table/tr[33]/td").extract_first()
            if pageresults:
                pageresults = pageresults.replace('\r', ''). \
                    replace('\n', '').replace('\t', ''). \
                    replace(' ', '').replace(u' ', '')
                getnum = re.search(r'/共(\d+)页查到记录共(\d+)条', pageresults)
                if getnum:
                    for i in range(1, int(getnum.group(1)) + 1):
                        nexturl = 'http://222.77.178.63:7002/result_new.asp?' \
                                  'page2=%d&xm_search=&zl_search=&gs_search=&' \
                                  'pzs_search=&pzx_search=&xzq_search=&bk_search=' % i
                        # req = Request(
                        #     url=nexturl,
                        #     meta={
                        #         'PageType': 'ProjectBase',
                        #     }
                        # )
                        # result.append(req)

                        project_base = {
                            'source_url': nexturl,
                            'meta': {'PageType': 'ProjectBase',
                                     }}
                        project_base_json = json.dumps(
                            project_base, sort_keys=True)
                        self.r.sadd('FuzhouCrawler:start_urls',
                                    project_base_json)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


#
'''
获取项目页面信息
'''


class GetProjectBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': '222.77.178.63:7002',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               }

    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://222.77.178.63:7002/'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('ProjectBase', 'SubProject'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'ProjectBase':
            results = response.xpath(
                "/html/body/table[1]/tr[2]/td/table/tr").extract()
            for get_result in results:
                if 'height="25"' in get_result:
                    get_result = get_result.replace('\r', ''). \
                        replace('\n', '').replace('\t', ''). \
                        replace(' ', '').replace(u' ', '')
                    myItems = re.findall(
                        ':#FFFFFF">(.*?)</td>', get_result, re.S)
                    Presalelicensenumber = myItems[0]
                    Projecturl = re.search(r'href="(.*?)"', myItems[1])
                    ProjectName = re.search(
                        r'target="_blank">(.*?)<', myItems[1])
                    if Projecturl and ProjectName:
                        new_url = self.shprojectmain_url + Projecturl.group(1)
                        result.append(Request(url=new_url,
                                              meta={
                                                  'PageType': 'SubProject',
                                                  # 'item': projectitem,
                                                  'Presalelicensenumber': Presalelicensenumber,
                                                  'lastname': ProjectName.group(1)
                                              },
                                              dont_filter=False))
        if response.meta.get('PageType') == 'SubProject':
            Presalelicensenumber = response.meta.get('Presalelicensenumber')
            projectinfobaseitem = ProjectinfoBaseItem()
            results = re.findall(
                r'align="left"(\s)class="indextabletxt">(.*?)</td>', response.text, re.S)
            try:
                Projectname = results[0][1]
                projectinfobaseitem['projectcounty'] = results[1][1]
                projectinfobaseitem['projectaddr'] = results[2][1]
                project_com_name = re.search(
                    '"_blank">(.*?)</a>', results[4][1], re.S).group(1)
                projectinfobaseitem['projectcomname'] = project_com_name
            except:
                Projectname = response.meta.get('lastname')
            projectinfobaseitem['Projectname'] = Projectname

            # result.append(projectitem)
            project_uuid = uuid.uuid3(uuid.NAMESPACE_DNS,
                                      str(Projectname + Presalelicensenumber)).hex
            projectinfobaseitem['projectuuid'] = str(project_uuid)

            price_results_div2 = response.xpath(
                '//*[@id="div2"]').extract_first()

            if price_results_div2 and '元' in price_results_div2:
                final_result = price_results_div2.replace('\r', '').replace('\n', '') \
                    .replace('\t', '').replace(' ', '').replace(u' ', '')

                price_results = re.findall(
                    r'ivalign="center">(.*?)</div>', final_result, re.S)
                projectinfobaseitem['projectprice'] = price_results[
                    0].replace("元", "")
                projectinfobaseitem['projectpricehouse'] = price_results[
                    1].replace("元", "")
                projectinfobaseitem['projectpriceback'] = price_results[
                    2].replace("元", "")
                projectinfobaseitem['projectpricehouseback'] = price_results[
                    3].replace("元", "")
            # //*[@id="div1"]/table
            price_results_div1 = response.xpath(
                '//*[@id="div1"]/table').extract_first()
            if price_results_div1:
                final_result1 = price_results_div1.replace('\r', '').replace('\n', '') \
                    .replace('\t', '').replace(' ', '').replace(u' ', '')
                total_infos = re.findall(r'dbgcolor="#999999">(.*?)</td><tdbgcolor="#CCCCCC">(.*?)</td>',
                                         final_result1, re.S)
                totalareas = total_infos[0][1].replace(",", "")
                totalhousenum = total_infos[1][1].replace(",", "")
                totalhouseareas = total_infos[2][1].replace(",", "")
                cansalenum = total_infos[3][1].replace(",", "")
                cansaleareas = total_infos[4][1].replace(",", "")
                cansalehousenum = total_infos[5][1].replace(",", "")
                cansalehouseareas = total_infos[6][1].replace(",", "")
                prebuynum = total_infos[7][1].replace(",", "")
                prebuyareas = total_infos[8][1].replace(",", "")
                prebuyhousenum = total_infos[9][1].replace(",", "")
                prebuyhouseareas = total_infos[10][1].replace(",", "")
                salednum = total_infos[11][1].replace(",", "")
                saledareas = total_infos[12][1].replace(",", "")
                saledhousenum = total_infos[13][1].replace(",", "")
                saledhouseareas = total_infos[14][1].replace(",", "")
                registerednum = total_infos[15][1].replace(",", "")
                registeredareas = total_infos[16][1].replace(",", "")
                registeredhousenum = total_infos[17][1].replace(",", "")
                registeredhouseareas = total_infos[18][1].replace(",", "")
                projectinfobaseitem['totalareas'] = int(totalareas)
                projectinfobaseitem['totalhousenum'] = int(totalhousenum)
                projectinfobaseitem['totalhouseareas'] = int(totalhouseareas)
                projectinfobaseitem['cansalenum'] = int(cansalenum)
                projectinfobaseitem['cansaleareas'] = int(cansaleareas)
                projectinfobaseitem['cansalehousenum'] = int(cansalehousenum)
                projectinfobaseitem['cansalehouseareas'] = int(
                    cansalehouseareas)
                projectinfobaseitem['prebuynum'] = int(prebuynum)
                projectinfobaseitem['prebuyareas'] = int(prebuyareas)
                projectinfobaseitem['prebuyhousenum'] = int(prebuyhousenum)
                projectinfobaseitem['prebuyhouseareas'] = int(prebuyhouseareas)
                projectinfobaseitem['salednum'] = int(salednum)
                projectinfobaseitem['saledareas'] = int(saledareas)
                projectinfobaseitem['saledhousenum'] = int(saledhousenum)
                projectinfobaseitem['saledhouseareas'] = int(saledhouseareas)
                projectinfobaseitem['registerednum'] = int(registerednum)
                projectinfobaseitem['registeredareas'] = int(registeredareas)
                projectinfobaseitem['registeredhousenum'] = int(
                    registeredhousenum)
                projectinfobaseitem['registeredhouseareas'] = int(
                    registeredhouseareas)
                Approvalcardturl = re.search(
                    "Presell.asp(.*?)'", response.text, re.S).group(1)
                Approvalcardturl = self.shprojectmain_url + 'Presell.asp' + Approvalcardturl
                projectinfobaseitem['ApprovalUrl'] = Approvalcardturl
                # 处理列表数据
                result.append(projectinfobaseitem)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


#

'''
处理预售证信息页面
'''


class OpenningunitBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    headers = {'Host': '222.77.178.63:7002',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               }

    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://222.77.178.63:7002/'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('openingunit'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'openingunit':
            projectno = response.meta['projectuuid']
            projectname = response.meta['Projectname']
            responsetext = response.body.decode('gbk', 'ignore').replace('\r', ''). \
                replace('\n', '').replace('\t', ''). \
                replace(' ', '').replace(' ', '')
            openingunitdetails = re.findall(
                r'indextabletxt(.*?)</TR>', responsetext)

            for openingunitdetail in openingunitdetails:
                if 'itemLine' in openingunitdetail:
                    approvalitem = ApprovalBaseItem()

                    approvalitem['projectno'] = str(projectno)
                    approvalitem['projectname'] = str(projectname)
                    item_details = re.findall(
                        r'height="19">(.*?)</td>', openingunitdetail)
                    opening_unit_no = re.search(
                        r'bold">(.*?)</span>', item_details[0]).group(1)
                    approvalitem['Approvalno'] = opening_unit_no
                    building_url = self.shprojectmain_url + 'building.asp' + re.search(
                        'building.asp(.*?)"', openingunitdetail, re.S).group(1)

                    approvalitem['Supervisionno'] = item_details[1]

                    approvalitem['Supervisionbank'] = item_details[2]
                    approvalitem['Approvaldate'] = item_details[3]
                    approvalitem['Totalnum'] = int(
                        item_details[4].replace(",", ""))
                    approvalitem['Totalhousenum'] = int(
                        item_details[5].replace(",", ""))

                    approvalitem['Totalareas'] = float(item_details[6].replace("m<SUP>2</SUP>", "").
                                                       replace("m<sup>2</sup>", ""))
                    approvalitem['Totalhouseareas'] = float(item_details[7].replace("m<SUP>2</SUP>", "").
                                                            replace("m<sup>2</sup>", ""))

                    result.append(approvalitem)
                    req = Request(url=building_url,
                                  meta={
                                      'PageType': 'buildingBase',
                                      'projectno': projectno,
                                      'projectname': projectname,
                                      'Approvalno': opening_unit_no
                                  },
                                  dont_filter=False)
                    result.append(req)
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

    headers = {'Host': '222.77.178.63:7002',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36'

               }

    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://222.77.178.63:7002/'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('buildingBase'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'buildingBase':
            projectno = response.meta.get('projectno')
            projectname = response.meta.get('projectname')
            Approvalno = response.meta.get('Approvalno')

            responsetext = response.body.decode('gbk', 'ignore')
            buildingrecod = []
            openingunitpagedetails = re.findall(
                r'class="indextabletxt">(.*?)</tr>', responsetext, re.S)
            for openingunitpagedetail in openingunitpagedetails:
                openingunitpagedetail = openingunitpagedetail.replace('\r', ''). \
                    replace('\n', '').replace('\t', ''). \
                    replace(' ', '').replace(u' ', '')
                buildingitemdetails = re.findall(r'tdalign="center"style="padding:3">(.*?)</td>',
                                                 openingunitpagedetail)
                # for buildingitemdetail in buildingitemdetails:
                #     print(buildingitemdetail)
                buildingitem = BuildingBaseItem()
                buildingitem['projectno'] = projectno
                buildingitem['projectname'] = projectname
                buildingitem['Approvalno'] = Approvalno

                get_building = re.search(
                    r'TARGET="_BLANK">(.*?)</a>', buildingitemdetails[0], re.S)
                if get_building:
                    buildingitem['buildingname'] = get_building.group(1)
                building_total_num = buildingitemdetails[1]
                if building_total_num:
                    buildingitem['buildingtotalnum'] = int(building_total_num)
                building_total_areas = buildingitemdetails[2]
                if building_total_areas:
                    buildingitem['buildingtotalareas'] = float(
                        building_total_areas)
                building_house_num = buildingitemdetails[3]
                if building_house_num:
                    buildingitem['buildinghousenum'] = int(building_house_num)
                building_house_areas = buildingitemdetails[4]
                if building_house_areas:
                    buildingitem['buildinghouseareas'] = float(
                        building_house_areas)
                building_detail_page_url = self.shprojectmain_url + 'House.asp' + re.search(
                    'House.asp(.*?)"', buildingitemdetails[0], re.S).group(1)

                if get_building:
                    if buildingitem['buildingname'] in buildingrecod:
                        building_no = uuid.uuid3(
                            uuid.NAMESPACE_DNS, str(building_detail_page_url)).hex
                    else:
                        building_no = uuid.uuid3(uuid.NAMESPACE_DNS, str(
                            Approvalno + buildingitem['buildingname'])).hex
                        buildingrecod.append(buildingitem['buildingname'])
                    buildingitem['buildingno'] = str(building_no)
                    buildingitem['house_url'] = building_detail_page_url
                    result.append(buildingitem)
                    req = Request(url=building_detail_page_url,
                                  meta={
                                      'PageType': 'HouseBase',
                                      'projectuuid': projectno,
                                      'projectname': projectname,
                                      'Approvalno': Approvalno,
                                      'building_no': str(building_no),
                                      'building_name': buildingitem['buildingname'],
                                  })
                    result.append(req)

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

    headers = {
        'Host': '222.77.178.63:7002',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    def __init__(self, settings):
        self.settings = settings
        self.shprojectmain_url = 'http://222.77.178.63:7002/'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseBase', 'HouseInfo'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'HouseBase':
            shprojectuuid = response.meta.get('projectuuid')
            projectname = response.meta.get('projectname')
            Approvalno = response.meta.get('Approvalno')
            building_no = response.meta.get('building_no')
            building_name = response.meta.get('building_name')
            building_detail_results = response.xpath(
                '//*[@id="Table1"]/tr/td/table[2]/tr').extract()
            house_sts_classify = {'#FF3399': '已签',
                                  '#FF0000': '已登记',
                                  '#00FF00': '可售',
                                  '#9999FF': '抵押',
                                  '#FFFF00': '限制',
                                  'FFFFFF': '未纳入网上销售',
                                  '#FFFFFF': '未纳入网上销售'
                                  }
            recnum = 0
            for building_detail_result in building_detail_results:
                building_detail_result = building_detail_result.replace('\r', ''). \
                    replace('\n', '').replace('\t', ''). \
                    replace(' ', '').replace(u' ', '')
                real_floor = re.search(
                    '<u>(.*?)</u>', building_detail_result, re.S).group(1)
                house_details = re.findall(
                    r'<tdbgco(.*?)</td>', building_detail_result)
                recordhouse = []
                for house_detail in house_details:
                    houseitem = HouseBaseItem()
                    houseitem['project_no'] = shprojectuuid
                    houseitem['project_name'] = projectname
                    houseitem['Approvalno'] = Approvalno
                    houseitem['building_no'] = building_no
                    houseitem['building_name'] = building_name
                    houseitem['house_floor'] = real_floor

                    house_type = re.search('lor="(.*?)"', house_detail, re.S)
                    if house_type:
                        house_sts = house_sts_classify[house_type.group(1)]
                    else:
                        house_sts = u'属于其它开盘单元'
                    recnum = recnum + 1
                    houseitem['house_sts'] = house_sts

                    house_area_pr_yc = re.search(
                        u'预测面积：(.*?)/', house_detail, re.S)
                    if house_area_pr_yc:
                        if len(house_area_pr_yc.group(1)) < 20:
                            houseitem[
                                'house_area_pr_yc'] = house_area_pr_yc.group(1)
                        else:
                            house_area_pr_yc = re.search(
                                u'预测面积：(.*?)平方米', house_detail, re.S)
                            houseitem[
                                'house_area_pr_yc'] = house_area_pr_yc.group(1)
                    house_area_real_yc = re.search(
                        u'实测面积(.*?)平方米', house_detail, re.S)
                    if house_area_real_yc:
                        houseitem['house_area_real_yc'] = house_area_real_yc.group(
                            1).replace(":", "").replace("：", "")
                    house_num = re.search(
                        r'"black">(.*?)</font>', house_detail, re.S)

                    if 'href' in house_detail:
                        if house_num:
                            house_num = str(house_num.group(1)).replace(
                                "（", "(").replace("）", ")")
                            houseitem['house_num'] = house_num
                        house_no = Approvalno + building_no + \
                            str(recnum) + real_floor
                    else:
                        house_num = re.search(
                            u'平方米">(.*?)<br>', house_detail, re.S)
                        if house_num:
                            house_num = str(house_num.group(1)).replace(
                                "（", "(").replace("）", ")")
                            houseitem['house_num'] = house_num
                        house_no = Approvalno + building_no + \
                            str(recnum) + real_floor
                    while house_no in recordhouse:
                        house_no = house_no + '1'
                    recordhouse.append(house_no)
                    houseitem['house_no'] = house_no
                    if house_sts == '可售':
                        house_detail_detail = re.search(
                            r'housedetail.asp(.*?)"', house_detail, re.S)
                        if house_detail_detail:
                            house_detail_page_url = self.shprojectmain_url + 'housedetail.asp' + house_detail_detail.group(
                                1).replace("amp;", "")
                            result.append(Request(
                                url=house_detail_page_url,
                                meta={
                                    'PageType': 'HouseInfo',
                                    'item': houseitem
                                },
                                dont_filter=False))
                    else:
                        result.append(houseitem)

        if response.meta.get('PageType') == 'HouseInfo':

            houseBaseitem = response.meta.get('item')
            houseitem = copy.deepcopy(houseBaseitem)
            house_use_type = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[4]/td[2]/text()').extract_first()
            if house_use_type:
                houseitem['house_use_type'] = house_use_type
            house_layout = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[5]/td[2]/text()').extract_first()
            if house_layout:
                houseitem['house_layout'] = house_layout
            house_area_pr_tn = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[7]/td[2]/text()').extract_first()
            if house_area_pr_tn:
                houseitem['house_area_pr_tn'] = house_area_pr_tn
            house_area_pr_ft = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[8]/td[2]/text()').extract_first()
            if house_area_pr_ft:
                houseitem['house_area_pr_ft'] = house_area_pr_ft
            house_area_pr_dx = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[9]/td[2]/text()').extract_first()
            if house_area_pr_dx:
                houseitem['house_area_pr_dx'] = house_area_pr_dx
            house_area_real_tn = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[11]/td[2]/text()').extract_first()
            if house_area_real_tn:
                houseitem['house_area_real_tn'] = house_area_real_tn
            house_area_real_ft = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[12]/td[2]/text()').extract_first()
            if house_area_real_ft:
                houseitem['house_area_real_ft'] = house_area_real_ft
            house_area_real_dx = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[13]/td[2]/text()').extract_first()
            if house_area_real_dx:
                houseitem['house_area_real_dx'] = house_area_real_dx
            house_price = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[15]/td[2]/text()').extract_first()
            if house_price:
                houseitem['house_price'] = house_price
            house_total_price = response.xpath(
                '//*[@id="Table1"]/tr/td/table/tbody/tr[16]/td[2]/text()').extract_first()
            if house_total_price:
                houseitem['house_total_price'] = house_total_price
            result.append(houseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return

# -*- coding: utf-8 -*-

import json
import logging
import sys
import traceback
import uuid

import regex
from HouseCrawler.Items.ItemsGuangzhou import *
from redis import Redis
from scrapy import Request, Selector

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse
logger = logging.getLogger(__name__)

debug = False
img_redis = Redis(host='10.30.2.11', port=6379, db=1)

# 从redis读取对应的key,将图片转数字


def imgToNumberText(NUMBER_IMG, dot, img_list):
    num = ''
    try:
        index = 0
        if isinstance(dot, list) and len(dot) > 0:
            index = dot[0].count('img src')
        for i in range(len(img_list)):
            num = num + str(NUMBER_IMG[img_list[i]])
            if i == int(index) - 1:
                num = num + '.'
    except:
        pass
    return num


class ProjectBaseHandleMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):

        def get_totla_page(string):
            total_page = 1
            if debug:
                return 1
            try:
                t = regex.search(r'共(\d+)页', string)
                total_page = int(t.group(1))
            except Exception:
                traceback.print_exc()
            return total_page

        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'ProjectBase':
            return result if result else []
        print('ProjectBaseHandleMiddleware')
        if response.meta.get('GetPage'):
            total_page = get_totla_page(response.body_as_unicode())
            for i in range(1, total_page + 1):
                url = 'http://www.gzcc.gov.cn/data/laho/ProjectSearch.aspx?page={curPage}'.format(
                    curPage=i)
                project_base_req = Request(
                    url=url,
                    headers=self.settings.getdict('DEFAULT_REQUEST_HEADERS'),
                    dont_filter=True,
                    meta={'PageType': 'ProjectBase'})
                result.append(project_base_req)
        else:
            tr_arr = response.xpath(
                '//table[@class="resultTableC"]/tbody/tr[not(@class)]')
            for tr in tr_arr:
                href = tr.xpath('td[2]/a/@href').extract_first(default="").strip()
                print(urlparse.urljoin(response.url, href))
                req = Request(
                    url=urlparse.urljoin(response.url, href),
                    headers=self.settings.getdict('DEFAULT_REQUEST_HEADERS'),
                    meta={'PageType': 'IframePage'})
                result.append(req)
        return result


class IframePageHandleMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def getParamsDict(url):
            query = urlparse.urlparse(url).query
            return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])
        if not (200 <= response.status < 300):  # common case
            print(response.status)
            return result if result else []
        if response.meta.get('PageType') != 'IframePage':
            return result if result else []
        print('IframePageHandleMiddleware')
        result = list(result)
        url_list = Selector(response).re(r'url = "(.+)";')
        project_info_url = urlparse.urljoin(response.url, url_list[0])
        ProjectID = project_info_url[project_info_url.rindex('=') + 1:]
        ProjectUUID = uuid.uuid3(uuid.NAMESPACE_DNS, project_info_url)
        ProjectName = response.xpath(
            '//div[@class="currentTitle"]/h3/text()').extract_first(default="")
        CertificateOfUseOfStateOwnedLand = ''
        ConstructionPermitNumber = ''
        BuildingPermit = ''

        CertificateOfUseOfStateOwnedLand_dict = getParamsDict(url_list[3])
        ConstructionPermitNumber_dict = getParamsDict(url_list[4])
        BuildingPermit_dict = getParamsDict(url_list[5])

        # 获取国土证/施工许可证/规划许可证的详细信息
        if 'country_name' in CertificateOfUseOfStateOwnedLand_dict:
            country_ids = CertificateOfUseOfStateOwnedLand_dict[
                'country_id'][:-1].split(',')
            country_names = CertificateOfUseOfStateOwnedLand_dict[
                'country_name'][:-1].split(',')
            url = 'http://www.gzcc.gov.cn/data/laho/country.aspx?country_name={country_name}&country_id={country_id}'
            for countryName, countryId in zip(country_names, country_ids):
                req = Request(url=url.format(country_name=str(countryName), country_id=str(countryName)),
                              headers=self.settings.getdict(
                                  'POST_DEFAULT_REQUEST_HEADERS'),
                              dont_filter=True,
                              meta={
                                  'PageType': 'Permit_CertificateOfUseOfStateOwnedLand',
                                  'ProjectID': ProjectID,
                                  'ProjectUUID': str(ProjectUUID),
                                  'countryId': countryId,
                                  'ProjectName': ProjectName
                })
                result.append(req)

        if 'agreeName' in ConstructionPermitNumber_dict:
            agreeIds = ConstructionPermitNumber_dict[
                'agreeId'][:-1].split(',')
            agreeNames = ConstructionPermitNumber_dict[
                'agreeName'][:-1].split(',')
            url = "http://www.gzcc.gov.cn/data/laho/workAgree.aspx?agreeName={agreeName}&agreeId={agreeId}"
            for agreeName, agreeId in zip(agreeNames, agreeIds):
                req = Request(url=url.format(agreeName=agreeName, agreeId=agreeId),
                              headers=self.settings.getdict(
                                  'POST_DEFAULT_REQUEST_HEADERS'),
                              dont_filter=True,
                              meta={
                                  'PageType': 'Permit_ConstructionPermitNumber',
                                  'ProjectID': ProjectID,
                                  'ProjectUUID': str(ProjectUUID),
                                  'agreeId': agreeId,
                                  'ProjectName': ProjectName
                })
                result.append(req)
        if 'layoutName' in BuildingPermit_dict:
            layoutNames = BuildingPermit_dict['layoutName'][:-1].split(',')
            layoutIds = BuildingPermit_dict['layoutId'][:-1].split(',')
            url = "http://www.gzcc.gov.cn/data/laho/layoutAgree.aspx?layoutName={layoutName}&layoutId={layoutId}&pjID={pjID}"
            for layoutName, layoutId in zip(layoutNames, layoutIds):
                req = Request(url=url.format(layoutName=layoutName, layoutId=layoutId, pjID=ProjectID),
                              headers=self.settings.getdict(
                                  'POST_DEFAULT_REQUEST_HEADERS'),
                              dont_filter=True,
                              meta={
                                  'PageType': 'Permit_BuildingPermit',
                                  'ProjectID': ProjectID,
                                  'ProjectUUID': str(ProjectUUID),
                                  'layoutId': layoutId,
                                  'ProjectName': ProjectName
                })
            result.append(req)

        # 获取项目详情
        projectInfo_req = Request(url=project_info_url,
                                  headers=self.settings.getdict(
                                      'DEFAULT_REQUEST_HEADERS'),
                                  dont_filter=True,
                                  meta={
                                      'PageType': 'ProjectInfo',
                                      'ProjectID': ProjectID,
                                      'ProjectUUID': str(ProjectUUID),
                                      'StreetInfoUrl': urlparse.urljoin(response.url, url_list[-1]),
                                      'CertificateOfUseOfStateOwnedLand': CertificateOfUseOfStateOwnedLand,
                                      'ConstructionPermitNumber': ConstructionPermitNumber,
                                      'BuildingPermit': BuildingPermit,
                                  })
        result.append(projectInfo_req)
        return result


class PermitInfoHandleMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def get_text(response, xpath):
            try:
                string = response.xpath(xpath).extract_first(default="").replace(u'\xa0', u' '). \
                    replace(' ', '').replace('\r', '').replace(
                        '\t', '').replace('\n', '').replace('　', '').strip()
                return string
            except:
                return ''

        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') not in (
                'Permit_CertificateOfUseOfStateOwnedLand', 'Permit_ConstructionPermitNumber', 'Permit_BuildingPermit'):
            return result if result else []
        print('PermitInfoHandleMiddleware')
        result = list(result)

        if response.meta.get('PageType') == 'Permit_CertificateOfUseOfStateOwnedLand':
            countryId = response.meta.get('countryId')
            permitInfoItem = PermitInfoItem()
            permitInfoItem['ProjectUUID'] = response.meta.get('ProjectUUID')
            permitInfoItem['ProjectID'] = response.meta.get('ProjectID')
            permitInfoItem['ProjectName'] = response.meta.get('ProjectName')
            permitInfoItem['PermitType'] = 'CertificateOfUseOfStateOwnedLand'
            permitInfoItem['PermitUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, permitInfoItem['ProjectID'] + permitInfoItem[
                'PermitType'] + countryId)

            permitInfoItem['Content'] = {
                '国土证号': get_text(response, '//td[starts-with(text(),"国土证号")]/following-sibling::td[1]/text()'),
                '土地座落': get_text(response, '//td[starts-with(text(),"土地座落")]/following-sibling::td[1]/text()'),
                '土地使用者': get_text(response, '//td[starts-with(text(),"土地使用者")]/following-sibling::td[1]/text()'),
                '地号': get_text(response, '//td[starts-with(text(),"地　号")]/following-sibling::td[1]/text()'),
                '图号': get_text(response, '//p[starts-with(text(),"图号")]/../following-sibling::td[1]/text()'),
                '土地用途': get_text(response, '//td[starts-with(text(),"土地用途")]/following-sibling::td[1]/text()'),
                '土地等级': get_text(response, '//td[starts-with(text(),"土地等级")]/following-sibling::td[1]/text()'),
                '土地出让年限自': get_text(response, '//td[starts-with(text(),"土地出让年限自")]/following-sibling::td[1]/text()'),
                '使用权类型': get_text(response, '//td[starts-with(text(),"使用权类型")]/following-sibling::td[1]/text()'),
                '使用权面积(平方米)': get_text(response, '//td[starts-with(text(),"使用权面积")]/following-sibling::td[1]/text()'),
                '其中共用分摊面积(平方米)': get_text(response,
                                          '//td[starts-with(text(),"其中共用分摊面积(平方米)")]/following-sibling::td[1]/text()'),
                '发证机关': get_text(response, '//td[starts-with(text(),"发证机关")]/following-sibling::td[1]/text()'),
                '发证日期': get_text(response, '//td[starts-with(text(),"发证日期")]/following-sibling::td[1]/text()'),
            }
            result.append(permitInfoItem)
        elif response.meta.get('PageType') == 'Permit_ConstructionPermitNumber':
            agreeId = response.meta.get('agreeId')
            permitInfoItem = PermitInfoItem()
            permitInfoItem['ProjectUUID'] = response.meta.get('ProjectUUID')
            permitInfoItem['ProjectID'] = response.meta.get('ProjectID')
            permitInfoItem['ProjectName'] = response.meta.get('ProjectName')
            permitInfoItem['PermitType'] = 'ConstructionPermitNumber'
            permitInfoItem['PermitUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, permitInfoItem['ProjectID'] + permitInfoItem[
                'PermitType'] + agreeId)
            permitInfoItem['Content'] = {
                '施工许可证号': get_text(response, '//td[starts-with(text(),"施工许可证号")]/following-sibling::td[1]/text()'),
                '发证日期': get_text(response, '//td[starts-with(text(),"发证日期")]/following-sibling::td[1]/text()'),
                '发证机关': get_text(response, '//td[starts-with(text(),"发证机关")]/following-sibling::td[1]/text()'),
                '工程名称': get_text(response, '//td[starts-with(text(),"工程名称")]/following-sibling::td[1]/text()'),
                '建设地址': get_text(response, '//td[starts-with(text(),"建设地址")]/following-sibling::td[1]/text()'),
                '建设单位': get_text(response, '//td[starts-with(text(),"建设单位")]/following-sibling::td[1]/text()'),
                '设计单位': get_text(response, '//td[starts-with(text(),"设计单位")]/following-sibling::td[1]/text()'),
                '施工单位': get_text(response, '//td[starts-with(text(),"施工单位")]/following-sibling::td[1]/text()'),
                '监理单位': get_text(response, '//td[starts-with(text(),"监理单位")]/following-sibling::td[1]/text()'),
                '合同价格(万元)': get_text(response, '//td[starts-with(text(),"合同价格")]/following-sibling::td[1]/text()'),
                '合同开工日期': get_text(response, '//td[starts-with(text(),"合同开工日期")]/following-sibling::td[1]/text()'),
                '合同竣工日期': get_text(response, '//td[starts-with(text(),"合同竣工日期")]/following-sibling::td[1]/text()'),
                '建设项目代表': get_text(response, '//td[starts-with(text(),"建设项目代表")]/following-sibling::td[1]/text()'),
                '设计项目负责人': get_text(response, '//td[starts-with(text(),"设计项目负责人：")]/following-sibling::td[1]/text()'),
                '注册项目经理': get_text(response, '//td[starts-with(text(),"注册项目经理：")]/following-sibling::td[1]/text()'),
                '注册项目总监': get_text(response, '//td[starts-with(text(),"注册项目总监：")]/following-sibling::td[1]/text()'),
                '地上层数': get_text(response, '//td[starts-with(text(),"地上层数：")]/following-sibling::td[1]/text()'),
                '地上幢数': get_text(response, '//td[starts-with(text(),"地上幢数：")]/following-sibling::td[1]/text()'),
                '地下层数': get_text(response, '//td[starts-with(text(),"地下层数：")]/following-sibling::td[1]/text()'),
                '地下幢数': get_text(response, '//td[starts-with(text(),"地下幢数：")]/following-sibling::td[1]/text()'),
            }
            result.append(permitInfoItem)
        elif response.meta.get('PageType') == 'Permit_BuildingPermit':
            layoutId = response.meta.get('layoutId')
            permitInfoItem = PermitInfoItem()
            permitInfoItem['ProjectUUID'] = response.meta.get('ProjectUUID')
            permitInfoItem['ProjectID'] = response.meta.get('ProjectID')
            permitInfoItem['ProjectName'] = response.meta.get('ProjectName')
            permitInfoItem['PermitType'] = 'BuildingPermit'
            permitInfoItem['PermitUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, permitInfoItem['ProjectID'] + permitInfoItem[
                'PermitType'] + layoutId)
            data = {
                '建设规划许可证号': get_text(response, '//td[starts-with(text(),"建设规划许可证号：")]/following-sibling::td[1]/text()'),
                '颁发机关': get_text(response, '//td[starts-with(text(),"颁发机关：")]/following-sibling::td[1]/text()'),
                '建设单位': get_text(response, '//td[starts-with(text(),"建设单位：")]/following-sibling::td[1]/p/text()'),
                '建设位置': get_text(response, '//td[starts-with(text(),"建设位置：")]/following-sibling::td[1]/p/text()'),
                '建设规模': get_text(response, '//td[starts-with(text(),"建设规模：")]/following-sibling::td[1]/p/text()'),
            }
            tr_arr = response.xpath('//tr[@bgcolor="#fff1da"]')
            for index, tr in enumerate(tr_arr):
                key = '项目' + str(index + 1)
                d = {
                    '主要功能': get_text(tr, './following-sibling::tr[1]/td[2]/p/text()'),
                    '地上层数': get_text(tr, './following-sibling::tr[2]/td[2]/p/text()'),
                    '地下层数': get_text(tr, './following-sibling::tr[3]/td[2]/p/text()'),
                    '幢数': get_text(tr, './following-sibling::tr[4]/td[2]/p/text()'),
                    '建筑高度(米)': get_text(tr, './following-sibling::tr[5]/td[2]/p/text()'),
                    '功能分布': get_text(tr, './following-sibling::tr[6]/td[2]/p/text()'),
                    '复式住宅分布': get_text(tr, './following-sibling::tr[7]/td[2]/p/text()'),
                    '栋号': get_text(tr, './following-sibling::tr[1]/td[4]/text()'),
                    '地上层面积(平方米)': get_text(tr, './following-sibling::tr[2]/td[4]/text()'),
                    '地下层面积(平方米)': get_text(tr, './following-sibling::tr[3]/td[4]/text()'),
                    '基底面积(平方米)': get_text(tr, './following-sibling::tr[4]/td[4]/text()'),
                    '居住户数(户)': get_text(tr, './following-sibling::tr[5]/td[4]/text()'),
                }
                data[key] = d
            permitInfoItem['Content'] = data
            result.append(permitInfoItem)
        return result


class ProjectInfoHandleMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') not in ('StreetInfo', 'ProjectInfo'):
            return result if result else []
        print('ProjectInfoHandleMiddleware', response.meta.get('PageType'))
        if response.meta.get('PageType') == 'StreetInfo':
            projectInfoItem = response.meta.get('projectInfoItem')
            try:
                t = regex.search(r'所属街道：(?<str>.+)\)</span>',
                                 response.body_as_unicode())
                projectInfoItem['RegionName'] = t.group(1)
            except:
                projectInfoItem['RegionName'] = ''
            result.append(projectInfoItem)
        else:
            ProjectID = response.meta.get('ProjectID')
            ProjectUUID = response.meta.get('ProjectUUID')
            CertificateOfUseOfStateOwnedLand = response.meta.get(
                'CertificateOfUseOfStateOwnedLand')
            ConstructionPermitNumber = response.meta.get(
                'ConstructionPermitNumber')
            BuildingPermit = response.meta.get('BuildingPermit')

            projectInfoItem = ProjectInfoItem()
            projectInfoItem['SourceUrl'] = response.url
            projectInfoItem['ProjectID'] = ProjectID
            projectInfoItem['ProjectUUID'] = ProjectUUID
            projectInfoItem[
                'CertificateOfUseOfStateOwnedLand'] = CertificateOfUseOfStateOwnedLand
            projectInfoItem[
                'ConstructionPermitNumber'] = ConstructionPermitNumber
            projectInfoItem['BuildingPermit'] = BuildingPermit
            projectInfoItem['ProjectName'] = response.xpath(
                '//td[starts-with(text(),"项目名称")]/following-sibling::td[1]/text()').extract_first(default="")
            projectInfoItem['PresalePermitNumber'] = response.xpath(
                '//td[starts-with(text(),"预售证")]/following-sibling::td[1]/text()').extract_first(default="")
            projectInfoItem['ProjectAddress'] = response.xpath(
                '//td[starts-with(text(),"项目地址")]/following-sibling::td[1]/text()').extract_first(default="")
            projectInfoItem['Developer'] = response.xpath(
                '//td[starts-with(text(),"开发商")]/following-sibling::td[1]/text()').extract_first(default="")
            projectInfoItem['DistrictName'] = response.xpath(
                '//td[starts-with(text(),"行政区划")]/following-sibling::td[1]/text()').extract_first(default="")
            projectInfoItem['FloorArea'] = response.xpath(
                '//td[starts-with(text(),"占地面积")]/following-sibling::td[1]/text()').extract_first(default="")
            projectInfoItem['TotalBuildingArea'] = response.xpath(
                '//td[starts-with(text(),"总建筑面积")]/following-sibling::td[1]/text()').extract_first(default="")
            projectInfoItem['QualificationNumber'] = response.xpath(
                '//td[starts-with(text(),"资质证书编号")]/following-sibling::td[1]/text()').extract_first(default="")
            temp = response.xpath(
                '//td[starts-with(text(),"用途性质")]/following-sibling::td[1]/text()').extract_first(default="")
            if temp != '':
                try:
                    temp = temp.replace('\xa0', ' ').replace('&nbsp;', '')
                except:
                    pass
            projectInfoItem['HouseUseType'] = temp

            presellCount = response.xpath(
                '//td[starts-with(text(),"批准预售套数")]/following-sibling::td[1]/text()').extract_first(default="").strip()
            projectInfoItem['ApprovalPresaleAmount'] = presellCount
            presellArea = response.xpath(
                '//td[starts-with(text(),"批准预售面积")]/following-sibling::td[1]/text()').extract_first(default="").strip()
            projectInfoItem['ApprovalPresaleArea'] = presellArea
            soldCount = response.xpath(
                '//td[starts-with(text(),"已售总套数")]/following-sibling::td[1]/text()').extract_first(default="").strip()
            projectInfoItem['TotalSoldAmount'] = soldCount
            unsoldCount = response.xpath(
                '//td[starts-with(text(),"未售总套数")]/following-sibling::td[1]/text()').extract_first(default="").strip()
            projectInfoItem['TotalUnsoldAmount'] = unsoldCount
            soldArea = response.xpath(
                '//td[starts-with(text(),"已售总面积")]/following-sibling::td[1]/text()').extract_first(default="").strip()
            projectInfoItem['TotalSoldArea'] = soldArea
            unsoldArea = response.xpath(
                '//td[starts-with(text(),"未售总面积")]/following-sibling::td[1]/text()').extract_first(default="").strip()
            projectInfoItem['TotalUnsoldArea'] = unsoldArea
            house_sold_count = response.xpath(
                '//td[text()="住宅"]/following-sibling::td[4]/text()').extract_first(default="").strip()
            house_sold_area = response.xpath(
                '//td[text()="住宅"]/following-sibling::td[5]/text()').extract_first(default="").strip()
            house_sold_price = response.xpath(
                '//td[text()="住宅"]/following-sibling::td[6]/text()').extract_first(default="").strip()
            house_unsold_count = response.xpath(
                '//td[text()="住宅"]/following-sibling::td[7]/text()').extract_first(default="").strip()
            house_unsold_area = response.xpath(
                '//td[text()="住宅"]/following-sibling::td[8]/text()').extract_first(default="").strip()
            business_sold_count = response.xpath(
                '//td[text()="商业"]/following-sibling::td[4]/text()').extract_first(default="").strip()
            business_sold_area = response.xpath(
                '//td[text()="商业"]/following-sibling::td[5]/text()').extract_first(default="").strip()
            business_sold_price = response.xpath(
                '//td[text()="商业"]/following-sibling::td[6]/text()').extract_first(default="").strip()
            business_unsold_count = response.xpath(
                '//td[text()="商业"]/following-sibling::td[7]/text()').extract_first(default="").strip()
            business_unsold_area = response.xpath(
                '//td[text()="商业"]/following-sibling::td[8]/text()').extract_first(default="").strip()
            office_sold_count = response.xpath(
                '//td[text()="办公"]/following-sibling::td[4]/text()').extract_first(default="").strip()
            office_sold_area = response.xpath(
                '//td[text()="办公"]/following-sibling::td[5]/text()').extract_first(default="").strip()
            office_sold_price = response.xpath(
                '//td[text()="办公"]/following-sibling::td[6]/text()').extract_first(default="").strip()
            office_unsold_count = response.xpath(
                '//td[text()="办公"]/following-sibling::td[7]/text()').extract_first(default="").strip()
            office_unsold_area = response.xpath(
                '//td[text()="办公"]/following-sibling::td[8]/text()').extract_first(default="").strip()
            parking_sold_count = response.xpath(
                '//td[text()="车位"]/following-sibling::td[4]/text()').extract_first(default="").strip()
            parking_sold_area = response.xpath(
                '//td[text()="车位"]/following-sibling::td[5]/text()').extract_first(default="").strip()
            parking_sold_price = response.xpath(
                '//td[text()="车位"]/following-sibling::td[6]/text()').extract_first(default="").strip()
            parking_unsold_count = response.xpath(
                '//td[text()="车位"]/following-sibling::td[7]/text()').extract_first(default="").strip()
            parking_unsold_area = response.xpath(
                '//td[text()="车位"]/following-sibling::td[8]/text()').extract_first(default="").strip()
            other_sold_count = response.xpath(
                '//td[text()="其他"]/following-sibling::td[4]/text()').extract_first(default="").strip()
            other_sold_area = response.xpath(
                '//td[text()="其他"]/following-sibling::td[5]/text()').extract_first(default="").strip()
            other_sold_price = response.xpath(
                '//td[text()="其他"]/following-sibling::td[6]/text()').extract_first(default="").strip()
            other_unsold_count = response.xpath(
                '//td[text()="其他"]/following-sibling::td[7]/text()').extract_first(default="").strip()
            other_unsold_area = response.xpath(
                '//td[text()="其他"]/following-sibling::td[8]/text()').extract_first(default="").strip()
            projectInfoItem[
                'HousingTotalSoldAmount'] = house_sold_count  # 住宅累计已售套数
            projectInfoItem[
                'HousingTotalSoldArea'] = house_sold_area  # 住宅累计已售面积
            projectInfoItem[
                'HousingTotalSoldPrice'] = house_sold_price  # 住宅累计已售均价
            projectInfoItem[
                'HousingUnsoldAmount'] = house_unsold_count  # 住宅未售套数
            projectInfoItem['HousinglUnsoldArea'] = house_unsold_area  # 住宅未售面积
            projectInfoItem[
                'ShopTotalSoldAmount'] = business_sold_count  # 商业累计已售套数
            projectInfoItem[
                'ShopTotalSoldArea'] = business_sold_area  # 商业累计已售面积
            projectInfoItem[
                'ShopTotalSoldPrice'] = business_sold_price  # 商业累计已售均价
            projectInfoItem[
                'ShopUnsoldAmount'] = business_unsold_count  # 商业未售套数
            projectInfoItem['ShoplUnsoldArea'] = business_unsold_area  # 商业未售面积
            projectInfoItem[
                'OfficeTotalSoldAmount'] = office_sold_count  # 办公累计已售套数
            projectInfoItem[
                'OfficeTotalSoldArea'] = office_sold_area  # 办公累计已售面积
            projectInfoItem[
                'OfficeTotalSoldPrice'] = office_sold_price  # 办公累计已售均价
            projectInfoItem[
                'OfficeUnsoldAmount'] = office_unsold_count  # 办公未售套数
            projectInfoItem['OfficelUnsoldArea'] = office_unsold_area  # 办公未售面积
            projectInfoItem[
                'ParkingTotalSoldAmount'] = parking_sold_count  # 车位累计已售套数
            projectInfoItem[
                'ParkingTotalSoldArea'] = parking_sold_area  # 车位累计已售面积
            projectInfoItem[
                'ParkingTotalSoldPrice'] = parking_sold_price  # 车位累计已售均价
            projectInfoItem[
                'ParkingUnsoldAmount'] = parking_unsold_count  # 车位未售套数
            projectInfoItem[
                'ParkinglUnsoldArea'] = parking_unsold_area  # 车位未售面积
            projectInfoItem[
                'OtherTotalSoldAmount'] = other_sold_count  # 其他累计已售套数
            projectInfoItem['OtherTotalSoldArea'] = other_sold_area  # 其他累计已售面积
            projectInfoItem[
                'OtherTotalSoldPrice'] = other_sold_price  # 其他累计已售均价
            projectInfoItem['OtherUnsoldAmount'] = other_unsold_count  # 其他未售套数
            projectInfoItem['OtherlUnsoldArea'] = other_unsold_area  # 其他未售面积
            house_sold_count = response.xpath(
                '//td[text()="住宅"]/following-sibling::td[1]/text()').extract_first(default="").strip()
            house_sold_area = response.xpath(
                '//td[text()="住宅"]/following-sibling::td[2]/text()').extract_first(default="").strip()
            house_check_out_count = response.xpath(
                '//td[text()="住宅"]/following-sibling::td[3]/text()').extract_first(default="").strip()
            business_sold_count = response.xpath(
                '//td[text()="商业"]/following-sibling::td[1]/text()').extract_first(default="").strip()
            business_sold_area = response.xpath(
                '//td[text()="商业"]/following-sibling::td[2]/text()').extract_first(default="").strip()
            business_check_out_count = response.xpath(
                '//td[text()="商业"]/following-sibling::td[3]/text()').extract_first(default="").strip()
            office_sold_count = response.xpath(
                '//td[text()="办公"]/following-sibling::td[1]/text()').extract_first(default="").strip()
            office_sold_area = response.xpath(
                '//td[text()="办公"]/following-sibling::td[2]/text()').extract_first(default="").strip()
            office_check_out_count = response.xpath(
                '//td[text()="办公"]/following-sibling::td[3]/text()').extract_first(default="").strip()
            parking_sold_count = response.xpath(
                '//td[text()="车位"]/following-sibling::td[1]/text()').extract_first(default="").strip()
            parking_sold_area = response.xpath(
                '//td[text()="车位"]/following-sibling::td[2]/text()').extract_first(default="").strip()
            parking_check_out_count = response.xpath(
                '//td[text()="车位"]/following-sibling::td[3]/text()').extract_first(default="").strip()
            other_sold_count = response.xpath(
                '//td[text()="其他"]/following-sibling::td[1]/text()').extract_first(default="").strip()
            other_sold_area = response.xpath(
                '//td[text()="其他"]/following-sibling::td[2]/text()').extract_first(default="").strip()
            other_check_out_count = response.xpath(
                '//td[text()="其他"]/following-sibling::td[3]/text()').extract_first(default="").strip()
            projectInfoItem['HousingSoldAmount'] = house_sold_count
            projectInfoItem['HousingSoldArea'] = house_sold_area
            projectInfoItem['HousingCheckoutAmount'] = house_check_out_count
            projectInfoItem['ShopSoldAmount'] = business_sold_count
            projectInfoItem['ShopSoldArea'] = business_sold_area
            projectInfoItem['ShopCheckoutAmount'] = business_check_out_count
            projectInfoItem['OfficeSoldAmount'] = office_sold_count
            projectInfoItem['OfficeSoldArea'] = office_sold_area
            projectInfoItem['OfficeCheckoutAmount'] = office_check_out_count
            projectInfoItem['ParkingSoldAmount'] = parking_sold_count
            projectInfoItem['ParkingSoldArea'] = parking_sold_area
            projectInfoItem['ParkingCheckoutAmount'] = parking_check_out_count
            projectInfoItem['OtherSoldAmount'] = other_sold_count
            projectInfoItem['OtherSoldArea'] = other_sold_area
            projectInfoItem['OtherCheckoutAmount'] = other_check_out_count

            # 获取街道
            street_req = Request(
                url=response.meta.get('StreetInfoUrl'),
                headers=self.settings.getdict('DEFAULT_REQUEST_HEADERS'),
                meta={'PageType': 'StreetInfo', 'projectInfoItem': projectInfoItem})
            result.append(street_req)

            # 预售证
            if projectInfoItem['PresalePermitNumber']:
                for i, ysz in enumerate(projectInfoItem['PresalePermitNumber'].split(',')):
                    presell_req = Request(url='http://www.gzcc.gov.cn/data/laho/preSell.aspx?pjID={pjID}&presell={preSell}&maxPrice=&groundPrice='.format(
                        pjID=projectInfoItem['ProjectID'],
                        preSell=ysz),
                        headers=self.settings.getdict(
                        'POST_DEFAULT_REQUEST_HEADERS'),
                        meta={'PageType': 'PresellInfo',
                              'ProjectID': projectInfoItem['ProjectID'],
                              'ProjectName': projectInfoItem['ProjectName'],
                              'ProjectUUID': str(projectInfoItem['ProjectUUID']),
                              'PresalePermitNumber': ysz})
                    result.append(presell_req)
        return result


# 预售证
class PresellInfoHandleMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'PresellInfo':
            return result if result else []
        print('PresellInfoHandleMiddleware')
        # presellInfoItem = response.meta.get('presellInfoItem')
        presellInfoItem = PresellInfoItem()
        presellInfoItem['ProjectID'] = response.meta.get('ProjectID')
        presellInfoItem['ProjectName'] = response.meta.get('ProjectName')
        presellInfoItem['ProjectUUID'] = response.meta.get('ProjectUUID')
        presellInfoItem['PresalePermitNumber'] = response.xpath(
            '//td/p[starts-with(text(),"预字第")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['PresellID'] = presellInfoItem['PresalePermitNumber']
        presellInfoItem['PresellUUID'] = uuid.uuid3(
            uuid.NAMESPACE_DNS, presellInfoItem['PresalePermitNumber'])
        presellInfoItem['PresaleBuildingAmount'] = response.xpath(
            '//td/p[starts-with(text(),"预售幢数")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['ConstructionFloorCount'] = response.xpath(
            '//td/p[starts-with(text(),"报建屋数")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['BuiltFloorCount'] = response.xpath(
            '//td/p[starts-with(text(),"已建层数")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['PeriodsCount'] = response.xpath(
            '//td/p[starts-with(text(),"本期期数")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['ConstructionTotalArea'] = response.xpath(
            '//td/p[starts-with(text(),"本期报建总面积")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['GroundArea'] = response.xpath(
            '//td/p[starts-with(text(),"地上面积")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['UnderGroundArea'] = response.xpath(
            '//td/p[starts-with(text(),"地下面积")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['PresaleUnitCount'] = response.xpath(
            '//td/p[starts-with(text(),"本期总单元套数")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['PresaleTotalBuildingArea'] = response.xpath(
            '//td/p[starts-with(text(),"本期预售总建筑面积")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['PresaleHousingLandIsMortgage'] = response.xpath(
            '//td/p[starts-with(text(),"预售房屋占用土地是否抵押")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['PresaleBuildingSupportingAreaInfo'] = response.xpath(
            '//td/p[starts-with(text(),"预售楼宇配套面积情况")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['LssueDate'] = response.xpath(
            '//td/p[starts-with(text(),"发证日期")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['LssuingAuthority'] = response.xpath(
            '//td/p[starts-with(text(),"发证机关")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['Contacts'] = response.xpath(
            '//td/p[starts-with(text(),"联系人")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['ValidityDateStartDate'] = response.xpath(
            '//td/p[starts-with(text(),"有效期自")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        presellInfoItem['ValidityDateClosingDate'] = response.xpath(
            '//td/p[starts-with(text(),"有效期至")]/../following-sibling::td[1]/p/text()').extract_first(default="")
        # 房屋分布
        house_count = response.xpath(
            '//table[2]/tr[3]/td[2]/text()').extract_first(default="")
        house_area = response.xpath(
            '//table[2]/tr[4]/td[2]/text()').extract_first(default="")
        business_count = response.xpath(
            '//table[2]/tr[3]/td[4]/text()').extract_first(default="")
        business_area = response.xpath(
            '//table[2]/tr[4]/td[4]/text()').extract_first(default="")
        office_count = response.xpath(
            '//table[2]/tr[3]/td[4]/text()').extract_first(default="")
        office_area = response.xpath(
            '//table[2]/tr[4]/td[4]/text()').extract_first(default="")
        parking_count = response.xpath(
            '//table[2]/tr[3]/td[5]/text()').extract_first(default="")
        parking_area = response.xpath(
            '//table[2]/tr[4]/td[5]/text()').extract_first(default="")
        other_count = response.xpath(
            '//table[2]/tr[3]/td[6]/text()').extract_first(default="")
        other_area = response.xpath(
            '//table[2]/tr[4]/td[6]/text()').extract_first(default="")
        tmp_dict = {'House': {'Count': house_count, 'Area': house_area},
                    'Shop': {'Count': business_count, 'Area': business_area},
                    'Office': {'Count': office_count, 'Area': office_area},
                    'Parking': {'Count': parking_count, 'Area': parking_area},
                    'Other': {'Count': other_count, 'Area': other_area}}
        presellInfoItem['HouseSpread'] = tmp_dict
        result.append(presellInfoItem)
        return result


class BuildingListHandleMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'BuildingList':
            return result if result else []
        print('BuildingListHandleMiddleware')
        ProjectID = response.meta.get('ProjectID')
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')
        td_list = response.xpath('//input[@name="buildingID"]/..')
        if td_list:
            for td in td_list:
                buildingID = td.xpath('input/@value').extract_first(default="")
                buildingName = td.re(r'\)">(.*)</td>')[0]
                buildingItem = BuildingInfoItem()
                buildingItem['ProjectUUID'] = ProjectUUID
                buildingItem['ProjectID'] = ProjectID
                buildingItem['ProjectName'] = ProjectName
                buildingItem['BuildingID'] = buildingID
                buildingItem['BuildingUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, ProjectUUID + buildingID)
                buildingItem['BuildingName'] = buildingName
                result.append(buildingItem)
                req_dict = {
                    'modeID': '1', 'hfID': '0', 'unitType': '0', 'houseStatusID': '0', 'totalAreaID': '0',
                    'inAreaID': '0', 'buildingID': str(buildingID)
                }
                building_req = Request(url='http://www.gzcc.gov.cn/housing/search/project/sellForm_pic.jsp',
                                       headers=self.settings.getdict(
                                           'POST_DEFAULT_REQUEST_HEADERS'),
                                       dont_filter=True,
                                       meta={
                                           'PageType': 'SellFormInfo',
                                           'ProjectID': ProjectID,
                                           'ProjectUUID': ProjectUUID,
                                           'ProjectName': ProjectName,
                                           'BuildingID': buildingID,
                                           'BuildingName': buildingName,
                                           'BuildingUUID': str(buildingItem['BuildingUUID']),
                                       },
                                       method='POST',
                                       body=urlparse.urlencode(req_dict))
                result.append(building_req)
        return result


class SellFormInfoHandleMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def getHouseLabel(response, font_list):
            if font_list:
                label_arr = []
                for font in font_list:
                    try:
                        text = response.xpath(
                            '//td[contains(text(),"' + font + '")]/text()').extract_first(default="")
                        text = text.replace(font, '')
                        label_arr.append(text)
                    except:
                        return ''
                return ','.join(label_arr)
            else:
                return ''
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'SellFormInfo':
            return result if result else []
        # print('SellFormInfoHandleMiddleware')
        ProjectID = response.meta.get('ProjectID')
        ProjectUUID = response.meta.get('ProjectUUID')
        ProjectName = response.meta.get('ProjectName')
        BuildingID = response.meta.get('BuildingID')
        BuildingUUID = response.meta.get('BuildingUUID')
        BuildingName = response.meta.get('BuildingName')
        check_isNullBuilding = False
        FloorCount = ''
        try:
            tmp = response.xpath(
                '//span[text()="暂时没有您想查看的数据"]/text()').extract_first(default="")
            if tmp:
                logger.info('项目id:%s,楼栋id：%s,楼栋名:%s没有户数据...' %
                            (ProjectID, BuildingID, BuildingName))
                check_isNullBuilding = True
            floor_text_arr = response.xpath(
                '//td[contains(text(),"层")]/text()').extract()
            FloorCount = floor_text_arr[0]
        except:
            pass
        if check_isNullBuilding:
            return result
        a_list = response.xpath('//a[contains(@href,"sellFormDetail.jsp")]')
        for a in a_list:
            href = 'http://www.gzcc.gov.cn/housing/search/project/' + \
                a.xpath('@href').extract_first(default="")
            HouseID = href[href.rindex('=') + 1:]
            HouseUUID = uuid.uuid3(uuid.NAMESPACE_DNS, href)
            font_list = a.xpath('font/text()').extract()
            HouseLabel = getHouseLabel(response, font_list)
            HouseState = ''
            try:
                title = a.xpath('@title').extract_first(default="")
                t = regex.search(r'当前状态：(.+)\n', title)
                HouseState = t.group(1)
            except:
                pass
            house_info_req = Request(url=href,
                                     headers=self.settings.getdict(
                                         'DEFAULT_REQUEST_HEADERS'),
                                     dont_filter=True,
                                     meta={'PageType': 'HouseInfo',
                                           'HouseID': HouseID,
                                           'HouseUUID': str(HouseUUID),
                                           'HouseLabel': HouseLabel,
                                           'HouseState': HouseState,
                                           'ProjectUUID': ProjectUUID,
                                           'ProjectName': ProjectName,
                                           'BuildingName': BuildingName,
                                           'BuildingUUID': BuildingUUID,
                                           'FloorCount': FloorCount,
                                           })
            result.append(house_info_req)
        return result


class HouseInfoHandleMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):  # common case
            return result if result else []
        if response.meta.get('PageType') != 'HouseInfo':
            return result if result else []
        # print('HouseInfoHandleMiddleware')
        houseDetailItem = HouseInfoItem()
        houseDetailItem['HouseID'] = response.meta.get('HouseID')
        houseDetailItem['HouseUUID'] = response.meta.get('HouseUUID')
        houseDetailItem['ProjectUUID'] = response.meta.get('ProjectUUID')
        houseDetailItem['ProjectName'] = response.meta.get('ProjectName')
        houseDetailItem['BuildingName'] = response.meta.get('BuildingName')
        houseDetailItem['BuildingUUID'] = response.meta.get('BuildingUUID')
        houseDetailItem['HouseState'] = response.meta.get('HouseState')
        houseDetailItem['HouseLabel'] = response.meta.get('HouseLabel')
        houseDetailItem['FloorCount'] = response.meta.get('FloorCount')
        houseDetailItem['SourceUrl'] = response.url

        houseDetailItem['HouseNumber'] = response.xpath(
            '//td[starts-with(text(),"房　　号")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['HouseName'] = response.xpath(
            '//td[starts-with(text(),"名义房号")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['HouseUseType'] = response.xpath(
            '//td[starts-with(text(),"房屋功能")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['ActualFloor'] = response.xpath(
            '//td[starts-with(text(),"实际层号")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['FloorName'] = response.xpath(
            '//td[starts-with(text(),"名义层号")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['FloorHight'] = response.xpath(
            '//td[starts-with(text(),"层高(米)")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['UnitShape'] = response.xpath(
            '//td[starts-with(text(),"房屋户型")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['IsPrivateUse'] = response.xpath(
            '//td[starts-with(text(),"是否自用")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['IsSharedPublicMatching'] = response.xpath(
            '//td[starts-with(text(),"是否公建配套")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['IsMoveBack'] = response.xpath(
            '//td[starts-with(text(),"是否回迁")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['BuildingStructure'] = response.xpath(
            '//td[starts-with(text(),"房屋结构")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['Balconys'] = response.xpath(
            '//td[starts-with(text(),"封闭阳台")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['UnenclosedBalconys'] = response.xpath(
            '//td[starts-with(text(),"非封闭阳台")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['Kitchens'] = response.xpath(
            '//td[starts-with(text(),"厨　　房")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['Toilets'] = response.xpath(
            '//td[starts-with(text(),"卫生间")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['IsMortgage'] = response.xpath(
            '//td[starts-with(text(),"是否抵押")]/following-sibling::td[1]/text()').extract_first(default="")
        houseDetailItem['IsAttachment'] = response.xpath(
            '//td[starts-with(text(),"是否查封")]/following-sibling::td[1]/text()').extract_first(default="")

        NUMBER_IMG = img_redis.get('NUMBER_IMG')
        if NUMBER_IMG:
            NUMBER_IMG = eval(NUMBER_IMG)
        else:
            logger.info('获取NUMBER_IMG失败，请检查redis中是否有数据！')
            result.append(houseDetailItem)
            return result
        yucezongmianji = response.xpath(
            '//td[starts-with(text(),"预测总面积")]/following-sibling::td[1]/text()').extract_first(default="").strip()
        houseDetailItem['ForecastBuildingArea'] = yucezongmianji
        shicezongmianji = response.xpath(
            '//td[starts-with(text(),"实测总面积")]/following-sibling::td[1]/text()').extract_first(default="").strip()
        houseDetailItem['MeasuredBuildingArea'] = shicezongmianji
        yucetaoneimianji = response.xpath(
            '//td[starts-with(text(),"预测套内面积")]/following-sibling::td[1]/text()').extract_first(default="").strip()
        houseDetailItem['ForecastInsideOfBuildingArea'] = yucetaoneimianji
        shicetaoneimianji = response.xpath(
            '//td[starts-with(text(),"实测套内面积")]/following-sibling::td[1]/text()').extract_first(default="").strip()
        houseDetailItem['MeasuredInsideOfBuildingArea'] = shicetaoneimianji
        yucegongtanmianji = response.xpath(
            '//td[starts-with(text(),"预测公摊面积")]/following-sibling::td[1]/text()').extract_first(default="").strip()
        houseDetailItem['ForecastPublicArea'] = yucegongtanmianji
        shicegongtanmianji = response.xpath(
            '//td[starts-with(text(),"实测公摊面积")]/following-sibling::td[1]/text()').extract_first(default="").strip()
        houseDetailItem['MeasuredSharedPublicArea'] = shicegongtanmianji
        result.append(houseDetailItem)
        return result

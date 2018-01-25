# coding = utf-8
import traceback
import urllib.parse as urlparse
import uuid

import regex
from HouseCrawler.Items.ItemsXA import *
from scrapy import Request


class BaseMiddleware(object):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Host': 'www.fang99.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
    }

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class ProjectBaseHandleMiddleware(BaseMiddleware):
    """
    1. 装填网站第一层所有链接地址；
    2. 解析网站第一层表结构；
    """

    @staticmethod
    def get_total_page(response):
        """
        获取 Base 层页码总数
        :param response: 响应报文
        :rtype : int
        """
        total_page = 0
        try:
            search_list = response.xpath('//*[@id="pager_buildingSearch"]/a/text()').extract()
            search_result = search_list[-2]
            if search_result:
                total_page = int(search_result)
        except Exception as e:
            traceback.print_exc()
        return total_page

    @staticmethod
    def get_building_id(href):
        """
        获取 Project ID (网站提供)
        :param href: url
        :rtype : int
        """
        result = 0
        try:
            result = regex.search(r'buildingid=(\d+)', href)
            if result:
                return result.group(1)
        except Exception:
            traceback.print_exc()
        return result

    def process_spider_output(self, response, result, spider):
        """
        - ProjectInitial: 装填链接地址
        - ProjectBase: 解析 Base 层信息
        :param response: 响应报文
        :param result: spider 解析结果
        :param spider: spider api
        :return : result
        """
        result = list(result)
        if not (200 <= response.status < 300):
            if result:
                return result
            return []

        if response.meta.get('PageType') not in ('ProjectInitial', 'ProjectBase'):
            if result:
                return result
            return []

        if response.meta.get('PageType') == 'ProjectInitial':
            print('ProjectBaseHandleMiddleware -- InitPages')
            page_count = self.get_total_page(response)
            req_list = []
            if page_count:
                for i in range(1, page_count + 1):
                    page_url = "http://www.fang99.com/buycenter/buildingsearch.aspx?page={}".format(i)
                    req_list.append(
                        Request(url=page_url, method='GET', headers=self.headers, meta={'PageType': 'ProjectBase'}))
            result.extend(req_list)

        elif response.meta.get('PageType') == 'ProjectBase':
            print('ProjectBaseHandleMiddleware')
            pro_list = response.xpath('//div[@class="sf_xf_prodiv"]')
            for div in pro_list:
                p_name = div.xpath('div[@class="sf_xf_projj ztys2"]/a[1]/text()').extract_first()
                room_type = div.xpath('div[@class="sf_xf_projj ztys2"]/font/@title').extract_first(default="")
                hot_house = div.xpath('div[@class="sf_xf_projj ztys2"]/text()[3]').extract_first(default="")
                project_address = div.xpath('div[@class="sf_xf_projj ztys2"]/text()[4]').extract_first()
                development_enterprise = div.xpath('div[@class="sf_xf_projj ztys2"]/div/a/text()').extract_first()
                telephone = div.xpath('div[@class="sf_xf_tel"]/text()').extract_first(default="")
                price = div.xpath('div[@class="sf_xf_tel"]/font/text()').extract_first()
                pb_href = div.xpath('div[@class="sf_xf_protp"]/a[1]/@href').extract_first()
                pb_url = 'http://www.fang99.com/buycenter/' + pb_href
                pj_id = self.get_building_id(pb_href)
                pjuuid = uuid.uuid3(uuid.NAMESPACE_DNS, p_name + str(pj_id))
                pb = ProjectBaseItem()
                pb['ProjectUUID'] = pjuuid
                pb['ProjectName'] = p_name
                pb['ProjectRoomType'] = room_type.replace("热销户型：", "")
                pb['ProjectHotSales'] = hot_house.replace("项目地址：", "")
                pb['ProjectAddress'] = project_address
                pb['ProjectCompany'] = development_enterprise
                pb['ProjectPhoneNum'] = telephone
                pb['ProjectPrice'] = price
                pb['ProjectBaseSubURL'] = pb_url
                result.append(pb)

        return result


class ProjectInfoHandleMiddleware(BaseMiddleware):
    """
    1. 处理 Base 层子页；
    2. 解析 Info 数据；
    """

    def process_spider_output(self, response, result, spider):
        """
        - ProjectBaseSub: 解析 Base 子页信息
        - ProjectInfo: 请求详情页并解析
        :param response: 响应报文
        :param result: spider 解析结果
        :param spider: spider api
        :return : result
        """
        result = list(result)
        if not (200 <= response.status < 400):  # common case
            if result:
                return result
            return []

        if response.meta.get('PageType') in ('ProjectSubBase', 'ProjectInfo',):
            if result:
                return result
            return []

        if response.meta.get('PageType') == 'ProjectSubBase':
            print('ProjectProjectSubBaseMiddleware')
            hand_tr = response.xpath(
                '//*[@id="jfsjdiv"]/table//tr/td[@bgcolor="#ffffff"]/..')
            hand_list = []
            for i, hand_build in enumerate(hand_tr):
                hand_key = hand_build.xpath(
                    'td[@width="100"]/text()').extract_first()
                if hand_key:
                    _hand_val = hand_build.xpath('td/a/text()').extract()
                    hand_val = ''.join(_hand_val).strip(' ').replace('、', ',')
                    hand_list.append(dict((hand_key, hand_val)))
            presale_href = response.xpath(
                '//*[@id="hplk_ysxkz"]/@href').extract_first()
            company_href = response.xpath(
                '//*[@id="kfslb"]/a[not(contains(href, "javascript"))]/@href').extract_first(default='')
            p_info_url = response.xpath(
                '//*[@id="bc_body"]/div/div/table/tr/td[@colspan="2"]/a[@style="color:#cd0001"]/@href').extract_first()
            item = ProjectInfoItem()
            item['ProjectUUID'] = response.meta.get('ProjectUUID', '')
            item['ProjectName'] = response.meta.get('ProjectName', '')
            item['ProjectCompany'] = response.meta.get('ProjectCompany', '')
            item['ProjectDueDate'] = hand_list
            item['ProjectInfoURL'] = p_info_url
            item['ProjectCompanyURL'] = 'http://www.fang99.com/buycenter/' + company_href
            item['ProjectPresaleURL'] = presale_href
            item['IsCompletion'] = '0'
            result.append(item)

        elif response.meta.get('PageType') == 'ProjectInfo':
            item = response.meta.get('item')
            # 基本信息
            item['ProjectAddress'] = response.xpath('//*[@id="Label_ProjectAdress"]/text()').extract_first()
            item['ProjectSalesAddress'] = response.xpath('//*[@id="lbl_SLDZ"]/text()').extract_first()
            item['ProjectCityArea'] = response.xpath('//*[@id="Label_CityArea"/text()]').extract_first()
            item['ProjectTradeCircle'] = response.xpath('//*[@id="Label_SQ"/text()]').extract_first()
            item['PropertyType'] = response.xpath('//*[@id="Label_Propertytypename"/text()]').extract_first()
            item['ProjectFirstDueDate'] = response.xpath(
                '//*[@id="bc_body"]/div/div/table/tr/td/table/tr/td[@class="sf_xq_jfsj"]/text()').extract_first(
                default='').strip()
            item['ProjectMainRoomType'] = response.xpath('//*[@id="Lable_Mainapirl"]/text()').extract_first()
            item['ProjectDekoration'] = response.xpath('//*[@id="Lable_Dekoration"]/text()').extract_first()
            item['ProjectBuildType'] = response.xpath('//*[@id="Lable_ConstructionType"]/text()').extract_first()
            # 项目简介
            item['ProjectBrief'] = response.xpath('//*[@id="lbl_Introduction"]/p/text()').extract_first()
            # 详细资料
            item['ProjectTotalFlat'] = response.xpath('//*[@id="lbl_ZTS"]/text()').extract_first()
            item['PropertyCost'] = response.xpath('//*[@id="lbl_WYF"]/text()').extract_first()
            item['ProjectSupplyType'] = response.xpath('//*[@id=""lbl_XFQF]/text()').extract_first()
            item['ProjectContainRoomType'] = response.xpath('//*[@id="lbl_BHHX"]/text()').extract_first()
            item['ProjectLoopLine'] = response.xpath('//*[@id="lbl_HXWZ"]/text()').extract_first()
            item['ProjectParkingSpace'] = response.xpath('//*[@id="lbl_TCW"]/text()').extract_first()
            item['LandUseLife'] = response.xpath('//*[@id="lbl_TDSYNX"]/text()').extract_first()
            # 周边配套
            # 单字段有多个属性
            education = response.xpath('//*[@id="lbl_School"]').extract_first(default='')
            commerce = response.xpath('//*[@id="lbl_Shop"]').extract_first(default='')
            bank = response.xpath('//*[@id="lbl_Bank"]').extract_first(default='')
            hospital = response.xpath('//*[@id="lbl_Hospital"]').extract_first(default='')
            traffic = response.xpath('//*[@id="lbl_Traffic"]').extract_first(default='')
            restaurant = response.xpath('//*[@id="lbl_CY"]').extract_first(default='')
            others = response.xpath('//*[@id="lbl_Others"]').extract_first(default='')
            item['PeripheryEducation'] = self.remove_html_tags_and_extract(education)
            item['PeripheryCommerce'] = self.remove_html_tags_and_extract(commerce)
            item['PeripheryBank'] = self.remove_html_tags_and_extract(bank)
            item['PeripheryHospital'] = self.remove_html_tags_and_extract(hospital)
            item['PeripheryTraffic'] = self.remove_html_tags_and_extract(traffic)
            item['PeripheryRestaurant'] = self.remove_html_tags_and_extract(restaurant)
            item['PeripheryOthers'] = self.remove_html_tags_and_extract(others)
            # 建筑形式
            item['BuildingStructure'] = response.xpath('//*[@id="lbl_JZJG"]/text()').extract_first()
            item['BuildingArea'] = response.xpath('//*[@id="lbl_JZMJ"]/text()').extract_first()
            item['BuildingFloorSpace'] = response.xpath('//*[@id="lbl_ZDMJ"]/text()').extract_first()
            item['MaxBuildingFlats'] = response.xpath('//*[@id="lbl_ZDDJ"]/text()').extract_first()
            item['MinBuildingFlats'] = response.xpath('//*[@id="lbl_ZXDJ"]/text()').extract_first()
            # 相关企业
            item['ProjectDevCompany'] = response.xpath('//*[@id="Label_WorkCompany"]/text()').extract_first()
            item['PropertyCompany'] = response.xpath('//*[@id="Label_PropertyCompany"]/text()').extract_first()
            item['IsCompletion'] = '1'
            result.append(item)
        return result

    @staticmethod
    def remove_html_tags_and_extract(node):
        pattern = regex.compile('<.*?>')
        text = regex.sub(pattern, '', node)
        return text


class PresaleLicenceHandleMiddleware(BaseMiddleware):
    """
    解析预售证页面
    """
    show_more_url = 'http://www.fang99.com/ashx/yszjjg.ashx'
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.fang99.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        'X-Requested-With': 'XMLHttpRequest',
    }

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):
            if result:
                return result
            return []
        if response.meta.get('PageType') in ('PresaleLicenceInfo', 'PresaleLicenceMore'):
            if result:
                return result
            return []

        if response.meta.get('PageType') == 'PresaleLicenceInfo':
            print('PresaleLicenceInfoHandleMiddleware')
            table_list = response.css('.fwzx_table_border > table')
            item_list = []
            project_id = response.meta.get('ProjectUUID', '')
            project_name = response.meta.get('ProjectName', '')
            for i, table in enumerate(table_list):
                _t1 = table.xpath('./tr/td[@bgcolor="#ffffff"][@class="fontYH"]/a/text()')
                _t2 = table.xpath('./tr/td[@bgcolor="#ffffff"][@class="fontYH"]/text()')
                item = PresaleLicenseInfoItem()
                item['ProjectUUID'] = project_id
                item['ProjectName'] = project_name
                item['PresaleCode'] = _t1.extract_first(default='')
                item['PresaleUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, item['ProjectUUID'] + item['PresaleCode'])
                item['BuildingRecordName'] = _t1.pop().extract() or ''
                item['DevCompany'] = _t2.extract()[0]
                item['LicenseDate'] = _t2.extract()[1]
                _t3 = table.xpath(
                    './tr/td[@style="border-collapse:collapse"]/table/tr/td[contains(@class, "fontYH")]/text()').extract()
                item['SuperviseBank'] = _t3[0]
                item['SuperviseBankAccount'] = _t3[1]
                building_list = table.xpath(
                    './tr/td[@bgcolor="#ffffff"]/table/tr/td[contains(@class, "fontYH")]/span/a')
                building_name_list = building_list.xpath('./text()').extract()
                item['BuildingList'] = ','.join(building_name_list)
                for j, building in enumerate(building_list):
                    building_name = building.xpath('./text()')
                    building_href = building.xpath('./@href')
                    if building_name:
                        b_item = BuildingInfoItem()
                        b_item['ProjectUUID'] = item['ProjectUUID']
                        b_item['ProjectName'] = item['ProjectName']
                        b_item['PresaleUUID'] = item['PresaleUUID']
                        b_item['BuildingURL'] = regex.sub('buildinglistselect', 'buildinglistselectpm', building_href)
                        b_item['BuildingName'] = building_name
                        b_item['BuildingUUID'] = uuid.uuid3(
                            uuid.NAMESPACE_DNS, project_id + item['PresaleUUID'] + building_name)
                        item_list.append(b_item)
                item_list.append(item)

            result.extend(item_list)
            show_more = response.xpath(
                '//*[@id="ck_table_0"]/img/@style').extract_first()
            if show_more != "display:none; margin-bottom:10px;":
                headers = self.headers
                headers['Referer'] = response.url
                req_dict = {"name": project_name, "yszh": "", "dwmc": ""}
                body = urlparse.urlencode(req_dict)
                meta = response.meta
                meta['PageType'] = 'PresaleLicenceInfo'
                r = Request(self.show_more_url, method="POST", body=body, meta=meta)
                result.append(r)

        elif response.meta.get('PageType') == 'PresaleLicenceMore':
            print('PresaleLicenceMoreHandleMiddleware')
            project_id = response.meta.get('ProjectUUID', '')
            project_name = response.meta.get('ProjectName', '')
            table_list = response.xpath('//table[@bgcolor="#dedede"]')
            item_list = []
            for i, table in enumerate(table_list):
                _t1 = table.xpath(
                    './tr/td[@bgcolor="#ffffff"][@class="fontYH"]/a/text()')
                _t2 = table.xpath(
                    '.tr/td[@bgcolor="#ffffff"][@class="fontYH"]/text()')
                item = PresaleLicenseInfoItem()
                item['ProjectUUID'] = project_id
                item['ProjectName'] = project_name
                item['PresaleCode'] = _t1.extract_first(default='')
                item['PresaleUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, item['ProjectUUID'] + item['PresaleCode'])
                item['BuildingRecordName'] = _t1.pop().extract() or ''
                item['DevCompany'] = _t2.extract()[0]
                item['LicenseDate'] = _t2.extract()[1]
                building_list = table.xpath(
                    './tr/td[@bgcolor="#ffffff"]/table/tr/td[contains(@class, "fontYH")]/span/a')
                building_name_list = building_list.xpath('./text()').extract()
                item['BuildingList'] = ','.join(building_name_list)
                _t3 = table.xpath(
                    './tr/td[@bgcolor="#ffffff"]/table/tr/td[contains(@class, "fontYH")]/text()').extract()
                _t3 = list(filter(lambda x: x != ',', _t3))
                item['SuperviseBank'] = _t3[0]
                item['SuperviseBankAccount'] = _t3[1]
                for j, building in enumerate(building_list):
                    building_name = building.xpath('./text()')
                    building_href = building.xpath('./@href')
                    if building_name:
                        b_item = BuildingInfoItem()
                        b_item['ProjectUUID'] = item['ProjectUUID']
                        b_item['ProjectName'] = item['ProjectName']
                        b_item['PresaleUUID'] = item['PresaleUUID']
                        b_item['BuildingURL'] = regex.sub('buildinglistselect', 'buildinglistselectpm', building_href)
                        b_item['BuildingName'] = building_name
                        b_item['BuildingUUID'] = uuid.uuid3(
                            uuid.NAMESPACE_DNS, project_id + item['PresaleUUID'] + building_name)

                        item_list.append(b_item)
            result.extend(item_list)


class HouseInfoHandleMiddleware(BaseMiddleware):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'b.fang99.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 310):
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseTable', 'HouseInfo'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'HouseTable':
            pages_obj = response.xpath('//*[@id="Anp_Housepager"]/a/text()')
            pages_obj.pop()
            _ = pages_obj.pop()
            total_page = int(_.get()) if _ else 0
            req_list = []
            for page in range(1, total_page + 1):
                url = response.url + '&page={}'.format(page)
                meta = response.meta
                meta['PageType'] = "HouseInfo"
                r = Request(url, headers=self.headers, meta=meta)
                req_list.append(r)
            result.extend(req_list)

        elif response.meta.get('PageType') == 'HouseInfo':
            print('HouseInfoHandleMiddleware')
            project_id = response.meta.get('ProjectUUID', '')
            project_name = response.meta.get('ProjectName', '')
            building_id = response.meta.get('BuildingUUID', '')
            building_name = response.meta.get('BuildingName', '')
            item_list = []
            t_row_list = response.xpath(
                '//*[@id="div_houselist"]/table/tr[@class="houselist hy"]')
            for i, row in enumerate(t_row_list):
                cells = row.xpath('./td/img/@src').re('prarm=(.*?)&')
                item = HouseInfoItem()
                item['ProjectUUID'] = project_id
                item['ProjectName'] = project_name
                item['BuildingUUID'] = building_id
                item['BuildingName'] = building_name
                room_no = self.extract_room_label(cells[0])
                build_no, unit_no = self.extract_building_and_unit_label(
                    cells[0])
                item['HouseRoomNum'] = room_no
                item['BuildingNum'] = build_no
                item['HouseUnit'] = unit_no
                item['HouseUUID'] = uuid.uuid3(
                    uuid.NAMESPACE_DNS, project_id + building_id + cells[0])
                item['HouseFloor'] = cells[1]
                item['HouseRoomType'] = cells[2]
                item['HouseUsage'] = cells[3]
                item['HouseType'] = cells[4]
                item['HouseBuildingArea'] = cells[5]
                item['HouseSaleState'] = row.xpath(
                    './td/div[@class="fwzt1_ygsf"]/text()').extract_first(default='')
                item_list.append(item)
            result.extend(item_list)
        return result

    @staticmethod
    def extract_building_and_unit_label(text):
        # BuildingNo. and UnitNo.
        bu = regex.search(r'(\d+)幢(\d+)单元', text)
        if bu:
            return bu.groups()
        else:
            return text, text

    @staticmethod
    def extract_room_label(text):
        # RoomNo.
        bu = regex.search(r'单元(.*)', text)
        if bu:
            return bu.group(1)
        else:
            return text

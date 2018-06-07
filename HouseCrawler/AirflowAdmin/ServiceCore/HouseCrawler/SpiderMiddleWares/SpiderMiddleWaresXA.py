# coding = utf-8
import traceback
import urllib.parse as urlparse
import uuid

import regex
from HouseCrawler.Items.ItemsXA import *
from scrapy import Request


class ProjectBaseHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def get_total_page(response):
            total_page = 0
            try:
                search_list = response.xpath('//*[@id="pager_buildingSearch"]/a/text()').extract()
                search_result = search_list[-2]
                if search_result:
                    total_page = int(search_result)
            except Exception as e:
                traceback.print_exc()
            return total_page

        def get_building_id(href):
            result = 0
            try:
                result = regex.search(r'buildingid=(\d+)', href)
                if result:
                    return result.group(1)
            except Exception:
                traceback.print_exc()
            return result

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
            page_count = get_total_page(response)
            if page_count:
                for i in range(1, page_count + 1):
                    page_url = "http://www.fang99.com/buycenter/buildingsearch.aspx?page={}".format(i)
                    result.append(
                        Request(url=page_url, method='GET',
                                headers=self.settings.get('DEFAULT_REQUEST_HEADERS'),
                                meta={'PageType': 'ProjectBase'}))


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
                pj_id = get_building_id(pb_href)
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


class ProjectInfoHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        def remove_html_tags_and_extract(node):
            pattern = regex.compile('<.*?>')
            text = regex.sub(pattern, '', node)
            return text

        result = list(result)
        if not (200 <= response.status < 302):  # common case
            if result:
                return result
            return []

        if response.meta.get('PageType') not in ('ProjectSubBase', 'ProjectInfo',):
            if result:
                return result
            return []

        if response.meta.get('PageType') == 'ProjectSubBase':
            print('ProjectProjectSubobject')
            item = ProjectInfoItem()

            hand_tr = response.xpath(
                '//*[@id="jfsjdiv"]/table//tr/td[@bgcolor="#ffffff"]/..')
            hand_list = []
            for i, hand_build in enumerate(hand_tr):
                hand_key = hand_build.xpath(
                    'td[@width="100"]/text()').extract_first('')
                if hand_key:
                    _hand_val = hand_build.xpath('td/a/text()').extract()
                    d = {}
                    hand_val = ''.join(_hand_val).strip(' ').replace('、', ',')
                    d[hand_key] = hand_val
                    hand_list.append(d)

            presale_href = response.xpath(
                '//*[@id="hplk_ysxkz"]/@href').extract_first()
            company_href = response.xpath(
                '//*[@id="kfslb"]/a[not(contains(@href, "javascript"))]/@href').extract_first(default='')
            p_info_url = response.xpath(
                '//*[@id="bc_body"]/div/div/table/tr/td[@colspan="2"]/a['
                '@style="color:#cd0001"]/@href').extract_first() or ''

            item['ProjectUUID'] = response.meta.get('ProjectUUID', '')
            item['ProjectName'] = response.meta.get('ProjectName', '')
            item['ProjectCompany'] = response.meta.get('ProjectCompany', '')
            item['ProjectDueDate'] = hand_list
            item['ProjectInfoURL'] = p_info_url
            item['ProjectCompanyURL'] = 'http://www.fang99.com/buycenter/' + company_href
            presale_href = "http://www.fang99.com" + presale_href if presale_href else ''
            item['ProjectPresaleURL'] = presale_href
            item['Point'] = response.xpath('//*[@id="hid_propoint"]/@value').extract_first(
                '//*[@id="hid_propoint"]/@value')
            item['ProjectBookingData'] = response.xpath('//*[@id="jfsjtd"]/text()').extract_first('').strip()
            item['AveragePrice'] = response.xpath('//*[@id="Label_AveragePrice"]/text()').extract_first('')
            result.append(Request(item['ProjectInfoURL'],
                                  meta={'PageType': 'ProjectInfo', 'item': item},
                                  headers=self.settings.get('DEFAULT_REQUEST_HEADERS')))
        elif response.meta.get('PageType') == 'ProjectInfo':
            item = response.meta.get('item')
            # 基本信息
            item['ProjectAddress'] = response.xpath('//*[@id="Label_ProjectAdress"]/text()').extract_first() or ''
            item['ProjectSalesAddress'] = response.xpath('//*[@id="lbl_SLDZ"]/text()').extract_first() or ''
            item['ProjectCityArea'] = response.xpath('//*[@id="Label_CityArea"]/text()').extract_first() or ''
            item['ProjectTradeCircle'] = response.xpath('//*[@id="Label_SQ"]/text()').extract_first() or ''
            item['PropertyType'] = response.xpath('//*[@id="Label_Propertytypename"]/text()').extract_first() or ''
            item['ProjectFirstDueDate'] = response.xpath(
                '//*[@id="bc_body"]/div/div/table/tr/td/table/tr/td[@class="sf_xq_jfsj"]/text()').extract_first(
                default='').strip()
            item['ProjectMainRoomType'] = response.xpath('//*[@id="Lable_Mainapirl"]/text()').extract_first() or ''
            item['ProjectDekoration'] = response.xpath('//*[@id="Lable_Dekoration"]/text()').extract_first() or ''
            item['ProjectBuildType'] = response.xpath('//*[@id="Lable_ConstructionType"]/text()').extract_first() or ''
            item['Decoration'] = response.xpath('//*[@id="Label_Dekoration"]/text()').extract_first() or ''
            # 项目简介
            item['ProjectBrief'] = response.xpath('//*[@id="lbl_Introduction"]/p/text()').extract_first() or ''
            # 详细资料
            item['ProjectTotalFlat'] = response.xpath('//*[@id="lbl_ZTS"]/text()').extract_first() or ''
            item['PropertyCost'] = response.xpath('//*[@id="lbl_WYF"]/text()').extract_first() or ''
            item['ProjectSupplyType'] = response.xpath('//*[@id="lbl_XFQF"]/text()').extract_first() or ''
            item['ProjectContainRoomType'] = response.xpath('//*[@id="lbl_BHHX"]/text()').extract_first() or ''
            item['ProjectLoopLine'] = response.xpath('//*[@id="lbl_HXWZ"]/text()').extract_first() or ''
            item['ProjectParkingSpace'] = response.xpath('//*[@id="lbl_TCW"]/text()').extract_first() or ''
            item['LandUseLife'] = response.xpath('//*[@id="lbl_TDSYNX"]/text()').extract_first() or ''
            # 周边配套
            # 单字段有多个属性
            education = response.xpath('//*[@id="lbl_School"]').extract_first(default='')
            commerce = response.xpath('//*[@id="lbl_Shop"]').extract_first(default='')
            bank = response.xpath('//*[@id="lbl_Bank"]').extract_first(default='')
            hospital = response.xpath('//*[@id="lbl_Hospital"]').extract_first(default='')
            traffic = response.xpath('//*[@id="lbl_Traffic"]').extract_first(default='')
            restaurant = response.xpath('//*[@id="lbl_CY"]').extract_first(default='')
            others = response.xpath('//*[@id="lbl_Others"]').extract_first(default='')
            item['PeripheryEducation'] = remove_html_tags_and_extract(education)
            item['PeripheryCommerce'] = remove_html_tags_and_extract(commerce)
            item['PeripheryBank'] = remove_html_tags_and_extract(bank)
            item['PeripheryHospital'] = remove_html_tags_and_extract(hospital)
            item['PeripheryTraffic'] = remove_html_tags_and_extract(traffic)
            item['PeripheryRestaurant'] = remove_html_tags_and_extract(restaurant)
            item['PeripheryOthers'] = remove_html_tags_and_extract(others)
            # 建筑形式
            item['BuildingStructure'] = response.xpath('//*[@id="lbl_JZJG"]/text()').extract_first() or ''
            item['BuildingArea'] = response.xpath('//*[@id="lbl_JZMJ"]/text()').extract_first(default='').replace('㎡',
                                                                                                                  '')
            item['BuildingFloorSpace'] = response.xpath('//*[@id="lbl_ZDMJ"]/text()').extract_first(
                default='').replace('㎡', '')
            item['MaxBuildingFlats'] = response.xpath('//*[@id="lbl_ZDDJ"]/text()').extract_first() or ''
            item['MinBuildingFlats'] = response.xpath('//*[@id="lbl_ZXDJ"]/text()').extract_first() or ''
            # 相关企业
            item['ProjectDevCompany'] = response.xpath('//*[@id="Label_DevName"]/text()').extract_first() or ''
            item['PropertyCompany'] = response.xpath('//*[@id="Label_PropertyCompany"]/text()').extract_first() or ''
            result.append(item)
        return result


class PresaleLicenceHandleMiddleware(object):
    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_spider_exception(self, response, exception, spider):
        return

    def process_spider_output(self, response, result, spider):
        result = list(result)
        if not (200 <= response.status < 300):
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('PresaleLicenceInfo', 'PresaleLicenceMore'):
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
                    uuid.NAMESPACE_DNS, str(item['ProjectUUID']) + item['PresaleCode'])
                item['BuildingRecordName'] = _t1.pop().extract() or ''
                item['DevCompany'] = _t2.extract()[0]
                item['LicenseDate'] = _t2.extract()[1]
                _t3 = table.xpath(
                    './tr/td[@style="border-collapse:collapse"]/table/tr/td[contains(@class, "fontYH")]/text('
                    ')').extract()
                item['SuperviseBank'] = _t3[0]
                item['SuperviseBankAccount'] = _t3[1]
                building_list = table.xpath(
                    './tr/td[@bgcolor="#ffffff"]/table/tr/td[contains(@class, "fontYH")]/span/a')
                building_name_list = building_list.xpath('./text()').extract()
                item['BuildingList'] = ','.join(building_name_list)
                for j, building in enumerate(building_list):
                    building_name = building.xpath('./text()').extract_first(default="")
                    building_href = building.xpath('./@href').extract_first(default="")
                    if building_name:
                        b_item = BuildingInfoItem()
                        b_item['ProjectUUID'] = item['ProjectUUID']
                        b_item['ProjectName'] = item['ProjectName']
                        b_item['PresaleUUID'] = item['PresaleUUID']
                        b_item['BuildingURL'] = regex.sub('buildinglistselect', 'buildinglistselectpm', building_href)
                        b_item['BuildingName'] = building_name
                        b_item['PresaleCode'] = item['PresaleCode']
                        b_item['BuildingUUID'] = uuid.uuid3(
                            uuid.NAMESPACE_DNS, str(project_id) + str(item['PresaleUUID']) + building_name)
                        item_list.append(b_item)
                item_list.append(item)

            result.extend(item_list)
            show_more = response.xpath(
                '//*[@id="ck_table_0"]/img/@style').extract_first()
            if show_more != "display:none; margin-bottom:10px;":
                req_dict = {"name": project_name, "yszh": "", "dwmc": ""}
                body = urlparse.urlencode(req_dict)
                meta = response.meta
                meta['PageType'] = 'PresaleLicenceInfo'
                r = Request('http://www.fang99.com/ashx/yszjjg.ashx', method="POST", body=body, meta=meta,
                            headers={
                                'Accept': 'text/plain, */*; q=0.01',
                                'Accept-Encoding': 'gzip, deflate',
                                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                                'Connection': 'keep-alive',
                                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                'Host': 'www.fang99.com',
                                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 '
                                              'Firefox/57.0',
                                'X-Requested-With': 'XMLHttpRequest',
                            })
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
                    uuid.NAMESPACE_DNS, str(item['ProjectUUID']) + item['PresaleCode'])
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
                    building_name = building.xpath('./text()').extract_first(default="")
                    building_href = building.xpath('./@href').extract_first(default="")
                    if building_name:
                        b_item = BuildingInfoItem()
                        b_item['ProjectUUID'] = item['ProjectUUID']
                        b_item['ProjectName'] = item['ProjectName']
                        b_item['PresaleUUID'] = item['PresaleUUID']
                        b_item['PresaleCode'] = item['PresaleCode']
                        b_item['BuildingURL'] = regex.sub('buildinglistselect', 'buildinglistselectpm', building_href)
                        b_item['BuildingName'] = building_name
                        b_item['BuildingUUID'] = uuid.uuid3(
                            uuid.NAMESPACE_DNS, str(project_id) + str(item['PresaleUUID']) + building_name)

                        item_list.append(b_item)
            result.extend(item_list)
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
        def extract_building_and_unit_label(text):
            # BuildingNo. and UnitNo.
            bu = regex.search(r'(\d+)幢(\d+)单元', text)
            if bu:
                return bu.groups()
            else:
                return text, text

        def extract_room_label(text):
            # RoomNo.
            bu = regex.search(r'单元(.*)', text)
            if bu:
                return bu.group(1)
            else:
                return text

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
            print('HouseInfoHandleMiddleware -- HouseTable')
            pages_obj = response.xpath('//*[@id="Anp_Housepager"]/a/text()')
            if pages_obj:
                pages_obj.pop()
                _ = pages_obj.pop()
                total_page = int(_.get()) if _ else 0
                req_list = []
                for page in range(1, total_page + 1):
                    url = response.url + '&page={}'.format(page)
                    meta = response.meta
                    meta['PageType'] = "HouseInfo"
                    r = Request(url, headers={
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': 'b.fang99.com',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
                        'X-Requested-With': 'XMLHttpRequest'
                    }, meta=meta)
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
                room_no = extract_room_label(cells[0])
                build_no, unit_no = extract_building_and_unit_label(
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
                item['HouseBuildingArea'] = cells[5].replace('㎡', '')
                item['HouseSaleState'] = row.xpath(
                    './td/div[starts-with(@class,"fwzt")]/text()').extract_first(default='')
                item_list.append(item)
            result.extend(item_list)
        return result

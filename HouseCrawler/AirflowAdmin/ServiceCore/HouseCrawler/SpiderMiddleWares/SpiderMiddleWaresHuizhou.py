# coding = utf-8
import sys, uuid, re
from scrapy import Request
from HouseCrawler.Items.ItemsHuizhou import *

if sys.version_info.major >= 3:
    import urllib.parse as urlparse
else:
    import urlparse

clean_rule1 = lambda x: x.strip().replace('\r', "") if x else ''
clean_rule2 = lambda x: x.strip().replace('\n', ";").replace('\r', "").replace('\t', '') if x else ''


def cheack_response(pagetype, response, result):
    if (response.meta.get('PageType') in pagetype) and (200 <= response.status < 300):

        out_come = 'right' if result else []

    else:
        out_come = result if result else []

    return out_come


class ProjectListMiddleware(object):
    headers = {"Host": "data.fz0752.com",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Upgrade-Insecure-Requests": "1",
               "Connection": "keep-alive",
               'Content-Type': 'application/x-www-form-urlencoded',
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

    def __init__(self, settings):

        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(pagetype=['pl_url'], response=response, result=result)

        if out_come == 'right':

            outcome_list, pagetype = [], response.meta['PageType']

            print('ProjectGetFidMiddleware')

            if pagetype == 'pl_url':

                content = response.xpath('//*[@id="searchResult"]/dd/div')

                now_page = int(response.xpath('//*[@id="searchResult"]/dt[2]/h2/div/text()').extract_first())

                crawler_page = response.xpath('//*[@id="searchResult"]/dt[2]/h2/a[10]/text()').re(r'\d+')[0]
                crawler_page = int(crawler_page)

                # 判断是否第一页,第一页进行翻页
                if now_page==1:
                    for page in range(2,crawler_page+1):
                        next_url = 'http://newhouse.fz0752.com/project/list.shtml?state=&key=&qy=&area=&danjia=&func=&fea=&type=&kp=&mj=&pageNO={0}'.format(
                            page)

                        list_req = Request(url=next_url, method='GET', headers=self.headers, meta={'PageType': 'pl_url'},
                                          dont_filter=True)

                        outcome_list.append(list_req)

                # 获取每页列表上的项目
                for i in content:
                    item_pd = Project_Detail_Item()

                    ProjectName = clean_rule1(i.xpath('./h1/span[1]/a/text()').extract_first())

                    ProjectUUID = uuid.uuid3(uuid.NAMESPACE_DNS, ProjectName)

                    ProjectUrl = clean_rule1(i.xpath('./h1/span[1]/a/@href').extract_first())

                    Developer = clean_rule1(i.xpath('./h2[2]/a/text()').extract_first())

                    phone = clean_rule1(i.xpath('./h4/span/text()').extract_first())

                    if ProjectUrl:
                        item_pd['ProjectName'] = ProjectName

                        item_pd['ProjectUUID'] = ProjectUUID

                        item_pd['ProjectUrl'] = ProjectUrl

                        item_pd['Developer'] = Developer

                        item_pd['SaleTelphoneNumber'] = phone

                        re_get = Request(url=item_pd['ProjectUrl'], method='GET', headers=self.headers,
                                         meta={'PageType': 'pd_url', "item": item_pd}, dont_filter=True)

                        outcome_list.append(re_get)
                # print(now_page, crawler_page)
                return outcome_list
        else:
            return out_come

    def process_spider_exception(self, response, exception, spider):
        return


class ProjectDetailMiddleware(object):

    headers = {"Host": "data.fz0752.com",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Upgrade-Insecure-Requests": "1",
               "Connection": "keep-alive",
               'Content-Type': 'application/x-www-form-urlencoded',
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(pagetype=['pd_url', 'pd_url2'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        def clean_district(status):
            if status in (
            "河南岸街道办", "江北街道办", "江南街道办", '桥东街道办', '桥西街道办', '水口街道办', '小金口街道办', '龙丰街道办', '汝湖镇', '马安镇', '三栋镇', '横沥镇',
            '芦洲镇'):
                return '惠城区'

            elif status in ("惠环街道办", "陈江街道办", "潼湖镇", "潼侨镇", "沥林镇", "东江科技园", "惠南科技园"):
                return '仲恺区'

            elif status in ("澳头街道办", "西区街道办", "霞涌街道办", "大亚湾中心区"):

                return "大亚湾"

            elif status in (
            "罗阳镇", "石湾镇", "罗浮山", "园洲镇", "龙溪镇", "杨村镇", "泰美镇", "长宁镇", "观音阁镇", "石坝镇", "麻陂镇", "公庄镇", "湖镇镇", "横河镇", "龙华镇",
            "福田镇", "柏塘镇", "杨侨镇"):

                return "博罗县"

            elif status in (
            "平山街道", "巽寮滨海旅游度假区", "港口滨海旅游度假区", "稔山镇", "平海镇", "黄埠镇", "多祝镇", "白花镇", "安墩镇", "大岭镇", "梁化镇", "铁涌镇", "吉隆镇",
            "宝口镇", "高潭镇", "白盆珠镇"):

                return "惠东县"

            else:
                return "龙门县"

        if (out_come == 'right') and (pagetype == 'pd_url'):

            item_pd = response.meta['item']

            url_next = response.xpath('//*[@id="house"]/div[7]/dl[3]/dt/div/a/@href').extract_first()

            re_get = Request(url=url_next, method='GET', headers=self.headers,
                             meta={'PageType': 'pd_url2', "item": item_pd}, dont_filter=True)

            outcome_list.append(re_get)

            return outcome_list


        elif (out_come == 'right') and (pagetype == 'pd_url2'):

            item_pd = response.meta['item']

            item_pd["RealEstateProjectID"] = re.findall(r'num\=(.+)', response.url)[0]

            item_pd['RegionName'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[1]/td[1]/text()').extract_first())

            item_pd['ProjectBlock'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[1]/td[2]/text()').extract_first())

            item_pd['BuildingType'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[2]/td[1]/text()').extract_first())

            item_pd['ProjectHouseType'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[2]/td[2]/text()').extract_first())

            item_pd["AveragePrice"] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[3]/td[1]/text()').extract_first())

            item_pd['ProjectMainShape'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[3]/td[2]/text()').extract_first())

            item_pd['FloorArea'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[4]/td[1]/text()').extract_first())

            item_pd['TotalBuidlingArea'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[4]/td[2]/text()').extract_first())

            item_pd['HouseBuildingCount'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[5]/td[1]/text()').extract_first())

            item_pd['HousingCount'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[5]/td[2]/text()').extract_first())

            item_pd['GreeningRate'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[6]/td[2]/text()').extract_first())

            item_pd['FloorAreaRatio'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[6]/td[1]/text()').extract_first())

            item_pd['PropertyRightsDescription'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[7]/td[2]/text()').extract_first())

            item_pd['ParkingSpaceAmount'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[8]/td[1]/text()').extract_first())

            item_pd['ParkingSpaceMatching'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[8]/td[2]/text()').extract_first())

            # item_pd['EarliestOpeningTime']   = clean_rule1(response.xpath('//*[@id="house"]/div[2]/div[5]/table/tr[8]/td[2]/text()').extract_first())

            # item_pd['FloorArea']             = clean_rule1(response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[4]/td[1]/text()').extract_first())

            item_pd['ProjectAddress'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[19]/td/text()').extract_first())

            item_pd['TotalBuidlingArea'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/tr[4]/td[2]/text()').extract_first())

            item_pd['ProjectLandNumber'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[2]/div[5]/table/tr[10]/td[2]/text()').extract_first())

            item_pd['ManagementFees'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[9]/td[2]/text()').extract_first())

            item_pd['ManagementCompany'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[9]/td[1]/text()').extract_first())

            item_pd['EarliestOpeningTime'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[10]/td[1]/text()').extract_first())

            item_pd['Project_LivingTime'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[10]/td[2]/text()').extract_first())

            item_pd['Decoration'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[12]/td[1]/text()').extract_first())

            item_pd['ProjectLandNumber'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[17]/td/text()').extract_first())

            item_pd['Project_Feature'] = clean_rule1(
                response.xpath('//*[@id="house"]/div[3]/dl[1]/dd/table/tr[20]/td/text()').extract_first())

            item_pd['Project_Traffic'] = clean_rule2(
                response.xpath('//*[@id="house"]/div[3]/dl[4]/dd/p[1]/text()').extract_first())

            item_pd['Project_Introduce'] = clean_rule2(
                response.xpath('//*[@id="house"]/div[3]/dl[2]/dd/p/text()').extract_first())

            item_pd['Project_Surround'] = clean_rule2(
                response.xpath('//*[@id="house"]/div[3]/dl[3]/dd/p[1]/text()').extract_first())

            item_pd['ProjectUrl'] = response.url

            item_pd['DistrictName'] = clean_district(item_pd['RegionName'])

            outcome_list.append(item_pd)

            return outcome_list


        else:

            return out_come

    def process_spider_exception(self, response, exception, spider):
        return


class BuildingDetailMiddleware(object):
    headers = {"Host": "data.fz0752.com",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Upgrade-Insecure-Requests": "1",
               "Connection": "keep-alive",
               'Content-Type': 'application/x-www-form-urlencoded',
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(pagetype=['bd_url', 'bd_url2'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        if (out_come == 'right') and (pagetype == 'bd_url'):

            cheack_key = response.xpath('//*[@id="house"]/div[3]/dl/dd/table/tr[2]/td/font/text()').extract_first()

            record_dict = response.meta['Record_Data']

            if cheack_key != '暂无数据！':

                BuildingItem = Building_Detail_Item()

                item_cd = Certificate_Detail_Item()

                BuildingItem['ProjectName'] = record_dict['ProjectName']

                BuildingItem['ProjectUUID'] = record_dict['ProjectUUID']

                item_cd['ProjectName'] = record_dict['ProjectName']

                item_cd['ProjectUUID'] = record_dict['ProjectUUID']

                content = response.xpath('//*[@id="house"]/div[3]/dl/dd/table/tr')

                for i in content[1:]:

                    item_cd['PresalePermitUrl'] = clean_rule1(i.xpath('./td[4]/a/@href').extract_first())

                    item_cd['PresalePermitNumber'] = clean_rule1(i.xpath('./td[4]/a/text()').extract_first())

                    BuildingItem['PresalePermitNumber'] = item_cd['PresalePermitNumber']
                    if item_cd['PresalePermitNumber'] !='':
                        item_cd['PresalePermitNumberUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS, item_cd['PresalePermitNumber'])
                        BuildingItem['PresalePermitNumberUUID'] = item_cd['PresalePermitNumberUUID']

                    BuildingItem['BuildingName'] = clean_rule1(i.xpath('./td[2]/span/text()').extract_first())

                    BuildingItem['BuildingNumber'] = clean_rule1(i.xpath('./td[3]/text()').extract_first())

                    BuildingItem['BuildingUrl'] = clean_rule1(i.xpath('./td[8]/a/@href').extract_first())
                    try:
                        BuildingItem['BuildingID'] = re.findall(r'bnum\=(.+?)\&', BuildingItem['BuildingUrl'])[0]
                    except Exception as e:
                        BuildingItem['BuildingID'] = re.findall(r'num\=(.+)?', BuildingItem['BuildingUrl'])[0]

                    BuildingItem['BuildingUUID'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                         BuildingItem['ProjectName'] + BuildingItem['BuildingName'] + BuildingItem[
                                                             'BuildingNumber'] + BuildingItem['PresalePermitNumber'])
                    BuildingItem['SourceUrl'] = response.url
                    outcome_list.append(BuildingItem)

                    cheack_key2 = re.findall(r'ysz_id', item_cd['PresalePermitUrl'])
                    if cheack_key2:

                        item_cd['PresalePermitUrl'] = 'http://newhouse.fz0752.com' + item_cd['PresalePermitUrl']

                        re_get2 = Request(url=item_cd['PresalePermitUrl'], method='GET', headers=self.headers,
                                          meta={'PageType': 'cd_url', "item": item_cd}, dont_filter=True)

                    else:
                        re_get2 = Request(url=item_cd['PresalePermitUrl'], method='GET', headers=self.headers,
                                          meta={'PageType': 'cd_url', "item": item_cd}, dont_filter=True)

                    outcome_list.append(re_get2)

                now_page = response.xpath('//*[@id="house"]/div[4]/div/span/text()').extract_first()

                next_page = int(now_page) + 1 if now_page else 0

                cheack_page = response.xpath(
                    '//*[@id="house"]/div[4]/div/a[contains(@href,"javascript:goPage({0})")]/@href'.format(
                        next_page)).extract()

                if cheack_page:
                    url_next = "http://newhouse.fz0752.com/project/selist.shtml?num={0}&old=&pageNO={1}".format(
                        record_dict['ProjectID'], next_page)

                    # print(url_next)

                    re_get = Request(url=url_next, method='GET', headers=self.headers,
                                     meta={'PageType': 'bd_url', "Record_Data": record_dict}, dont_filter=True)

                    outcome_list.append(re_get)

            return outcome_list

        else:
            # print('BuildingDetailMiddlewareover')
            return out_come

    def process_spider_exception(self, response, exception, spider):

        return


class CertificateDetailMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(pagetype=['cd_url'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        if out_come == 'right':

            item_cd = response.meta['item']

            cheack_key = re.findall(r'ysz_id\=(.+)', response.url)

            if cheack_key:

                item_cd['DeveloperPermitNumber'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[3]/td/text()').extract_first())

                item_cd['LandNumberAndUse'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[6]/td/text()').extract_first())

                item_cd['PresaleTotalBuidlingArea'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[7]/td[1]/text()').extract_first())

                item_cd['PresaleHouseCount'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[7]/td[2]/text()').extract_first())

                item_cd['LivingArea'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[8]/td[1]/text()').extract_first())

                item_cd['BusinessArea'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[9]/td[1]/text()').extract_first())

                item_cd['OtherArea'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[10]/td[1]/text()').extract_first())

                item_cd['PresaleBuildingNo'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[8]/td[2]/text()').extract_first())

                item_cd['BuiltFloorCount'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[9]/td[2]/text()').extract_first())

                item_cd['PresaleHousingLandIsMortgage'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[10]/td[2]/text()').extract_first())

                item_cd['ValidityDateStartDate'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[11]/td[1]/text()').extract_first())

                item_cd['ValidityDateClosingDate'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[11]/td[2]/text()').extract_first())

                item_cd['LssuingAuthority'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[12]/td[1]/text()').extract_first())

                item_cd['LssueDate'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[12]/td[2]/text()').extract_first())

                item_cd['Bank_Account'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[4]/table/tbody/tr[13]/td/text()').extract_first())

                item_cd['Remarks'] = ''

                outcome_list.append(item_cd)

            else:

                item_cd['DeveloperPermitNumber'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[2]/td[4]/text()').extract_first())

                item_cd['LandNumberAndUse'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[5]/td[2]/text()').extract_first())

                item_cd['PresaleTotalBuidlingArea'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[6]/td[2]/text()').extract_first())

                item_cd['PresaleHouseCount'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[6]/td[4]/text()').extract_first())

                item_cd['LivingArea'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[7]/td[3]/text()').extract_first())

                item_cd['BusinessArea'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[8]/td[2]/text()').extract_first())

                item_cd['OtherArea'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[9]/td[2]/text()').extract_first())

                item_cd['PresaleBuildingNo'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[7]/td[5]/text()').extract_first())

                item_cd['BuiltFloorCount'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[8]/td[4]/text()').extract_first())

                item_cd['PresaleHousingLandIsMortgage'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[9]/td[4]/text()').extract_first())

                item_cd['ValidityDateStartDate'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[10]/td[2]/text()').extract_first())

                item_cd['ValidityDateClosingDate'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[10]/td[2]/text()').extract_first())

                item_cd['LssuingAuthority'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[11]/td[2]/text()').extract_first())

                item_cd['LssueDate'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[11]/td[4]/text()').extract_first())

                item_cd['Bank_Account'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[12]/td[2]/text()').extract_first())

                item_cd['Remarks'] = clean_rule1(
                    response.xpath('/html/body/center/div[2]/div[5]/table/tr[13]/td[2]/text()').extract_first())

                outcome_list.append(item_cd)

            return outcome_list


        else:
            # print('over')

            return out_come

    def process_spider_exception(self, response, exception, spider):
        return


class HouseDetailMiddleware(object):

    def __init__(self, settings):
        self.settings = settings
        self.headers = {"Host": "data.fz0752.com",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Connection": "keep-alive",
                   "Upgrade-Insecure-Requests": "1",
                   "Connection": "keep-alive",
                   'Content-Type': 'application/x-www-form-urlencoded',
                   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        def cheack_status(status):
            status_dict = {
                '/fontHtml/images/house/ks.gif':'可售',
                '/fontHtml/images/house/ysqy.gif':'已签预售合同',
                '/fontHtml/images/house/ba.gif':'已备案',
                '/fontHtml/images/house/bks.gif':'不可售',
                '/fontHtml/images/house/ybz.gif':'已办证',
                '/fontHtml/images/house/bzz.gif':'办证中',
                '/fontHtml/images/house/cq1.gif':'草签',
                '/fontHtml/images/house/xfqy.gif':'现房签约',
                '/fontHtml/images/house/yyg.gif':'已预告',
                '/fontHtml/images/house/xfyba.gif':'现房已预告',
            }
            return status_dict.get(status,status)

        out_come = cheack_response(pagetype=['hd_url', 'hd_url2'], response=response, result=result)

        if (out_come == 'right') and (response.meta['PageType'] == 'hd_url'):

            outcome_list, record_dict = [], response.meta['Record_Data']

            url_list = response.xpath('//table[@class="textCenter" and @bgcolor]/tr')

            for i in url_list[2:]:
                item_hd = House_Detail_Item()

                item_hd['ProjectUUID'] = record_dict['ProjectUUID']

                item_hd['BuildingUUID'] = record_dict['BuildingUUID']

                item_hd['ProjectName'] = record_dict['ProjectName']

                item_hd['BuildingName'] = record_dict['BuildingName']

                item_hd['BuildingNumber'] = record_dict['BuildingNumber']

                item_hd["PresalePermitNumberUUID"] = record_dict["PresalePermitNumberUUID"]

                item_hd['SourceUrl'] = response.url

                item_hd['HouseName'] = i.xpath('./td[not(@rowspan)][1]/text()').extract_first()

                item_hd['ForecastBuildingArea'] = i.xpath('./td[not(@rowspan)][2]/text()').extract_first()

                item_hd['ForecastInsideOfBuildingArea'] = i.xpath('./td[not(@rowspan)][3]/text()').extract_first()

                item_hd['MeasuredBuildingArea'] = i.xpath('./td[not(@rowspan)][4]/text()').extract_first()

                item_hd['MeasuredInsideOfBuildingArea'] = i.xpath('./td[not(@rowspan)][5]/text()').extract_first()

                item_hd['SalePriceByBuildingArea'] = i.xpath('./td[not(@rowspan)][6]/text()').extract_first()

                item_hd['SalePriceByBuildingArea'] = i.xpath('./td[not(@rowspan)][7]/text()').extract_first()

                item_hd['HouseSaleState'] = cheack_status(i.xpath('./td[not(@rowspan)][8]/img/@src').extract_first())

                item_hd['HouseUrl'] = 'http://data.fz0752.com' + i.xpath(
                    './td[not(@rowspan)][9]/a/@href').extract_first()

                item_hd['HouseID'] = re.search(r'num\=(\d+)', item_hd['HouseUrl']).group(1) if item_hd[
                    'HouseUrl'] else ''

                houseuuid_raw = item_hd['ProjectName'] + item_hd['BuildingName'] + item_hd['BuildingNumber'] + str(
                    item_hd["PresalePermitNumberUUID"]) + item_hd['HouseID']

                item_hd['HouseUUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, houseuuid_raw))


                houseDetail_req = Request(url = '',headers=self.headers,
                        meta={
                            'PageType' : 'hd_url2',
                            'Item':item_hd
                        })

                outcome_list.append(houseDetail_req)

            return outcome_list


        elif (out_come == 'right') and (response.meta['PageType'] == 'hd_url2'):

            outcome_list = []

            item_hd = response.meta['Item']

            item_hd['HouseUseType'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[4]/td[4]/text()').extract_first())

            item_hd['HouseUse'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[5]/td[2]/text()').extract_first())

            item_hd['UnitShape'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[5]/td[4]/text()').extract_first())

            item_hd['FloorName'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[6]/td[2]/text()').extract_first())

            item_hd['FloorHight'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[6]/td[4]/text()').extract_first())

            item_hd['Toward'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[7]/td[2]/text()').extract_first())

            item_hd['BuildingStructure'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[7]/td[4]/text()').extract_first())

            item_hd['IsPublicMating'] = clean_rule1(
                response.xpath(' /html/body/center/div[2]/div[5]/table/tr[8]/td[2]/text()').extract_first())

            item_hd['IsMoveBack'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[8]/td[4]/text()').extract_first())

            item_hd['IsPrivateUse'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[9]/td[2]/text()').extract_first())

            item_hd['IsPermitSale'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[9]/td[4]/text()').extract_first())

            item_hd['Balconys'] = clean_rule1(
                response.xpath(' /html/body/center/div[2]/div[5]/table/tr[12]/td[2]/text()').extract_first())

            item_hd['UnenclosedBalconys'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[12]/td[4]/text()').extract_first())

            item_hd['Kitchens'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[13]/td[2]/text()').extract_first())

            item_hd['Toilets'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[13]/td[4]/text()').extract_first())

            item_hd['SalePriceList'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[10]/td[2]/text()').extract_first())

            item_hd['ForecastPublicArea'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[17]/td[2]/text()').extract_first())

            item_hd['MeasuredBuildingArea'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[15]/td[4]/text()').extract_first())

            item_hd['MeasuredInsideOfBuildingArea'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[16]/td[4]/text()').extract_first())

            item_hd['MeasuredSharedPublicArea'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[17]/td[4]/text()').extract_first())

            item_hd['IsMortgage'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[19]/td[2]/text()').extract_first())

            item_hd['IsAttachment'] = clean_rule1(
                response.xpath('/html/body/center/div[2]/div[5]/table/tr[19]/td[4]/text()').extract_first())


            outcome_list.append(item_hd)

            return outcome_list

        else:
            # print('over')

            return out_come

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class MonitorMiddleware(object):

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        out_come = cheack_response(pagetype=['monitor'], response=response, result=result)

        outcome_list, pagetype = [], response.meta['PageType']

        if out_come == 'right':

            item = Monitor_Item()

            item['riqi'] = clean_rule1(
                response.xpath('//tr[@style="background: #F5F5F5;"][10]/td[1]/text()').extract_first())

            item['wangshangqianyue_taoshu'] = clean_rule1(
                response.xpath('//tr[@style="background: #F5F5F5;"][10]/td[2]/text()').extract_first())

            item['wangshangqianyue_mianji'] = clean_rule1(
                response.xpath('//tr[@style="background: #F5F5F5;"][10]/td[3]/text()').extract_first())

            item['wangshangqianyue_zhuzhaitaoshu'] = clean_rule1(
                response.xpath('//tr[@style="background: #F5F5F5;"][10]/td[4]/text()').extract_first())

            item['wangshangqianyue_zhuzhaimianji'] = clean_rule1(
                response.xpath('//tr[@style="background: #F5F5F5;"][10]/td[5]/text()').extract_first())

            item['wangshangqianyuedengji_taoshu'] = clean_rule1(
                response.xpath('//tr[@style="background: #F5F5F5;"][10]/td[6]/text()').extract_first())

            item['wangshangqianyuedengji_mianji'] = clean_rule1(
                response.xpath('//tr[@style="background: #F5F5F5;"][10]/td[7]/text()').extract_first())

            item['wangshangqianyuedengji_zhuzhaitaoshu'] = clean_rule1(
                response.xpath('//tr[@style="background: #F5F5F5;"][10]/td[8]/text()').extract_first())

            item['wangshangqianyuedengji_zhuzhaimianji'] = clean_rule1(
                response.xpath('//tr[@style="background: #F5F5F5;"][10]/td[9]/text()').extract_first())

            # print(item)

            outcome_list.append(item)

            return outcome_list

        else:

            return out_come

    def process_spider_exception(self, response, exception, spider):

        return
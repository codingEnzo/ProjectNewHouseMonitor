try:
    import sys
    import re
    import copy
    import traceback
    import redis
    import uuid
    from scrapy import Request
    from scrapy import Selector
    import random
    from HouseNew.models import *
    from HouseCrawler.Items.ItemsSZ import *
    if sys.version_info.major >= 3:
        import urllib.parse as urlparse
    else:
        import urlparse
except Exception:
    traceback.print_exc()
contextflag = True
# http://www.szfcweb.com/


def check_data_str(string):
    fix_result = ''
    if string:
        fix_result = string.strip()
        fix_data = {'\r': '',
                    '\n': '',
                    '\t': '',
                    ' ': ''
                    }
        for r in fix_data:
            fix_result = fix_result.strip().replace(r, fix_data[r])
    return fix_result

'''
获取预售证信息
'''


class GetYszBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Host': 'www.szfcweb.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': random.choice(setting.USER_AGENTS)
        }

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        def get_total_page(string):
            total_page = ''
            total_num = ''
            page_num = ''
            try:
                search_result = re.search(
                    r'共&nbsp(.*?)&nbsp条&nbsp--&nbsp第&nbsp(.*?)&nbsp页&nbsp--&nbsp共&nbsp(.*?)&nbsp页',
                    str(string))
                if search_result:
                    total_num = search_result.group(1)
                    page_num = search_result.group(2)
                    total_page = search_result.group(3)
            except Exception as e:
                traceback.print_exc()
            return total_num, page_num, total_page

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('GetYszBase', 'GetYszInfoBase', 'GetYszDataInfoBase'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'GetYszBase':
            if response.request.method == 'GET':
                addr = response.meta.get('addr')
                VIEWSTATE = Selector(response).xpath(
                    '//*[@id="__VIEWSTATE"]/@value').extract_first()
                EVENTVALIDATION = Selector(response).xpath(
                    '//*[@id="__EVENTVALIDATION"]/@value').extract_first()
                EVENTARGUMENT = Selector(response).xpath(
                    '//*[@id="__EVENTARGUMENT"]/@value').extract_first()
                LASTFOCUS = Selector(response).xpath(
                    '//*[@id="__LASTFOCUS"]/@value').extract_first()
                req_dict = {
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': EVENTARGUMENT,
                    '__LASTFOCUS': LASTFOCUS,
                    '__VIEWSTATE': VIEWSTATE,
                    '__EVENTVALIDATION': EVENTVALIDATION,
                    'ctl00$MainContent$txt_Pro': '',
                    'ctl00$MainContent$txt_Com': '',
                    'ctl00$MainContent$ddl_RD_CODE': addr,
                    'ctl00$MainContent$txt_ysz': '',
                    'ctl00$MainContent$bt_select': '查询',
                    'ctl00$MainContent$PageGridView1$ctl12$PageList': 0
                }
                req_body = urlparse.urlencode(req_dict)
                result.append(Request(url=response.url, body=req_body, headers=self.headers, method='POST', meta={'PageType': 'GetYszBase',
                                                                                                                  'item': addr}))

                return result
            elif response.request.method == 'POST':
                projectallitem = ProjectallItem()
                total_num, page_num, page_count = get_total_page(
                    response.body_as_unicode())
                VIEWSTATE = Selector(response).xpath(
                    '//*[@id="__VIEWSTATE"]/@value').extract_first()
                EVENTVALIDATION = Selector(response).xpath(
                    '//*[@id="__EVENTVALIDATION"]/@value').extract_first()
                EVENTARGUMENT = Selector(response).xpath(
                    '//*[@id="__EVENTARGUMENT"]/@value').extract_first()
                LASTFOCUS = Selector(response).xpath(
                    '//*[@id="__LASTFOCUS"]/@value').extract_first()
                project_area = response.meta.get('item')
                projectallitem['project_add'] = project_area
                projectallitem['project_num'] = total_num
                result.append(projectallitem)
                for page in range(0, int(page_count)):
                    req_dict = {
                        '__EVENTTARGET': 'ctl00$MainContent$PageGridView1$ctl12$PageList',
                        '__EVENTARGUMENT': EVENTARGUMENT,
                        '__LASTFOCUS': LASTFOCUS,
                        '__VIEWSTATE': VIEWSTATE,
                        '__EVENTVALIDATION': EVENTVALIDATION,
                        'ctl00$MainContent$txt_Pro': '',
                        'ctl00$MainContent$txt_Com': '',
                        'ctl00$MainContent$ddl_RD_CODE': response.meta.get('item'),
                        'ctl00$MainContent$txt_ysz': '',
                        'ctl00$MainContent$PageGridView1$ctl12$PageList': page
                    }
                    newheader = self.headers
                    newheader['Referer'] = response.url
                    req_body = urlparse.urlencode(req_dict)
                    # if contextflag:
                    #     project_base = {
                    #         'source_url': response.url,
                    #         'headers': newheader,
                    #         'body': req_body, 'method': 'POST',
                    #         'meta': {'PageType': 'GetYszInfoBase',
                    #                  'retrytimes': 0}}
                    #     project_base_json = json.dumps(project_base, sort_keys=True)
                    #     self.r.sadd('SuzhouCrawler:start_urls', project_base_json)
                    result.append(Request(url=response.url,
                                          headers=newheader,
                                          body=req_body,
                                          method='POST',
                                          meta={
                                              'PageType': 'GetYszInfoBase',

                                          }))
        if response.meta.get('PageType') == 'GetYszInfoBase':
            PresaleUrls = re.findall(
                r"MITShowView.aspx\?(.*?)'", response.body_as_unicode())
            if PresaleUrls:
                for PresaleUrl in PresaleUrls[1:]:
                    result.append(Request(url=str(response.url).replace("MITShowList.aspx", "MITShowView.aspx?") + PresaleUrl.replace("amp;", ""),
                                          headers=self.headers,
                                          method='GET',
                                          meta={
                                              'PageType': 'GetYszDataInfoBase'
                    }))
        if response.meta.get('PageType') == 'GetYszDataInfoBase':
            approvalbaseitem = ApprovalBaseItem()

            # //*[@id="ctl00_MainContent_lb_RD_Code"]
            PresaleRDCode = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_RD_Code"]/text()').extract_first()

            # //*[@id="ctl00_MainContent_lb_PP_PYear"]
            PresalePPPYear = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_PP_PYear"]/text()').extract_first()

            # //*[@id="ctl00_MainContent_lb_PP_PSN"]
            PresalePP_PSN = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_PP_PSN"]/text()').extract_first()
            PresalePermitNumber = '苏房预' + check_data_str(PresaleRDCode) + check_data_str(
                PresalePPPYear) + check_data_str(PresalePP_PSN) + '号'
            approvalbaseitem['PresalePermitNumber'] = PresalePermitNumber
            # //*[@id="ctl00_MainContent_lb_PP_CORPName"]
            PresalePPCORPName = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_PP_CORPName"]/text()').extract_first()
            approvalbaseitem['PresalePPCORPName'] = PresalePPCORPName
            # //*[@id="ctl00_MainContent_lb_Pro_Name"]
            PresaleProName = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_Pro_Name"]/text()').extract_first()
            approvalbaseitem['PresaleProName'] = PresaleProName
            # //*[@id="ctl00_MainContent_lb_Pro_Address"]
            PresaleProAddress = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_Pro_Address"]/text()').extract_first()
            approvalbaseitem['PresaleProAddress'] = PresaleProAddress

            # //*[@id="ctl00_MainContent_lb_Pre_SumArea"]
            PresalePreSumArea = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_Pre_SumArea"]/text()').extract_first()
            approvalbaseitem['PresalePreSumArea'] = PresalePreSumArea
            # //*[@id="ctl00_MainContent_lb_ZG_Area"]
            PresaleZGArea = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_ZG_Area"]/text()').extract_first()
            approvalbaseitem['PresaleZGArea'] = PresaleZGArea
            # //*[@id="ctl00_MainContent_lb_ZG_Count"]
            PresaleZGCount = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_ZG_Count"]/text()').extract_first()
            approvalbaseitem['PresaleZGCount'] = PresaleZGCount
            # //*[@id="ctl00_MainContent_lb_FZG_Area"]
            PresaleFZGArea = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_FZG_Area"]/text()').extract_first()
            approvalbaseitem['PresaleFZGArea'] = PresaleFZGArea
            # //*[@id="ctl00_MainContent_lb_FZG_Count"]
            PresaleFZGCount = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_FZG_Count"]/text()').extract_first()
            approvalbaseitem['PresaleFZGCount'] = PresaleFZGCount
            # //*[@id="ctl00_MainContent_lb_QT_Area"]
            PresaleQTArea = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_QT_Area"]/text()').extract_first()
            approvalbaseitem['PresaleQTArea'] = PresaleQTArea
            # //*[@id="ctl00_MainContent_lb_QT_Count"]
            PresaleQTCount = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_QT_Count"]/text()').extract_first()
            approvalbaseitem['PresaleQTCount'] = PresaleQTCount
            # //*[@id="ctl00_MainContent_lb_PP_IDate"]
            PresalePPIDate = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_PP_IDate"]/text()').extract_first()
            approvalbaseitem['PresalePPIDate'] = PresalePPIDate
            # //*[@id="ctl00_MainContent_lb_JZ_IDate"]
            PresaleJZIDate = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_JZ_IDate"]/text()').extract_first()
            approvalbaseitem['PresaleJZIDate'] = PresaleJZIDate
            if PresaleProName:
                result.append(approvalbaseitem)
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


'''
获取所有项目链接信息
'''


class GetProjectBaseHandleMiddleware(object):

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Host': 'pf.szfcweb.com',
            'Origin': 'http://spf.szfcweb.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36'

        }

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        def get_total_page(string):
            total_page = ''
            total_num = ''
            try:

                search_result = re.search(r'共&amp;nbsp(.*?)&amp;nbsp条&amp;nbsp--&amp;nbsp第&amp;nbsp(.*?)&amp;nbsp页&amp;nbsp--&amp;nbsp共&amp;nbsp(.*?)&amp;nbsp页',
                                          str(string))
                if search_result:
                    total_num = search_result.group(1)
                    total_page = search_result.group(3)

            except Exception:
                traceback.print_exc()
            return total_num, total_page

        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('GetProjectBase'):
            if result:
                return result
            return []
        if response.request.method == 'GET':

            req_list = []
            VIEWSTATE = Selector(response).xpath(
                '//*[@id="__VIEWSTATE"]/@value').extract_first()
            VIEWSTATEGENERATOR = Selector(response).xpath(
                '//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
            EVENTVALIDATION = Selector(response).xpath(
                '//*[@id="__EVENTVALIDATION"]/@value').extract_first()

            req_dict = {
                '__VIEWSTATE': VIEWSTATE,
                '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
                '__EVENTVALIDATION': EVENTVALIDATION,
                'ctl00$MainContent$txt_Pro': '',
                'ctl00$MainContent$txt_Com': '',
                'ctl00$MainContent$bt_select': '查询',
            }
            addr = response.meta.get('addr')
            # for addr in addrs:
            #     req_dict['ctl00$MainContent$ddl_RD_CODE'] = addr
            #     req_body = urlparse.urlencode(req_dict)
            #     req_list.append(Request(url=response.url, body=req_body, headers=headers, method='POST'
            #                             , meta={'PageType': 'GetProjectBase',
            #                                     'item': addr}))
            req_dict['ctl00$MainContent$ddl_RD_CODE'] = addr
            req_body = urlparse.urlencode(req_dict)
            req_list.append(Request(url=response.url,
                                    body=req_body,
                                    headers=self.headers,
                                    method='POST',
                                    meta={
                                        'PageType': 'GetProjectBase',
                                        'item': addr
                                    }))
            return req_list
        elif response.request.method == 'POST':
            projectallitem = ProjectallItem()
            page_body = Selector(response).xpath(
                '//*[@id="aspnetForm"]/div[3]/table/tr[2]/td/table').extract_first()
            total_num, page_count = get_total_page(page_body)
            VIEWSTATE = Selector(response).xpath(
                '//*[@id="__VIEWSTATE"]/@value').extract_first()
            VIEWSTATEGENERATOR = Selector(response).xpath(
                '//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
            EVENTVALIDATION = Selector(response).xpath(
                '//*[@id="__EVENTVALIDATION"]/@value').extract_first()
            EVENTARGUMENT = Selector(response).xpath(
                '//*[@id="__EVENTARGUMENT"]/@value').extract_first()
            LASTFOCUS = Selector(response).xpath(
                '//*[@id="__LASTFOCUS"]/@value').extract_first()
            project_area = response.meta.get('item')
            projectallitem['project_add'] = project_area
            projectallitem['project_num'] = total_num
            result.append(projectallitem)
            headers = self.headers
            headers['Referer'] = response.url
            for page in range(0, int(page_count)):
                req_dict = {
                    '__EVENTTARGET': 'ctl00$MainContent$OraclePager1$ctl12$PageList',
                    '__VIEWSTATE': VIEWSTATE,
                    '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
                    '__EVENTVALIDATION': EVENTVALIDATION,
                    '__EVENTARGUMENT': EVENTARGUMENT,
                    '__LASTFOCUS': LASTFOCUS,
                    'ctl00$MainContent$txt_Pro': '',
                    'ctl00$MainContent$ddl_RD_CODE': response.meta.get('item'),
                    'ctl00$MainContent$txt_Com': '',
                    'ctl00$MainContent$OraclePager1$ctl12$PageList': page
                }

                req_body = urlparse.urlencode(req_dict)
                # if contextflag:
                #     project_base = {
                #         'source_url': response.url,
                #         'headers': headers,
                #         'body': req_body,
                #         'method': 'POST',
                #         'meta': {
                #             'PageType': 'ProjectPageBase',
                #         }
                #     }
                #
                #     project_base_json = json.dumps(project_base, sort_keys=True)
                #     self.r.sadd('SuzhouCrawler:start_urls', project_base_json)
                result.append(Request(url=response.url,
                                      body=req_body,
                                      headers=headers,
                                      method='POST',
                                      meta={
                                          'PageType': 'ProjectPageBase',
                                      }))

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return

'''
获取具体项目信息
'''


class GetProjectPageBaseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)
        # getnum = random.randint(0, 9)
        # self.getkey = str(self.r.get('SuzhouCrawlerkey%d' % getnum)).replace("b'", "").replace("'", "")

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
        if response.meta.get('PageType') not in ('ProjectPageBase', 'ProjectPageBaseNext'):
            if result:
                return result
            return []

        if response.request.method == 'POST':
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Host': 'pf.szfcweb.com',
                'Origin': 'http://spf.szfcweb.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': response.url,
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36'

            }

            main_url = str(response.url).replace(
                "SaleInfoProListIndex.aspx", "")
            Datas = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_OraclePager1"]/tr')
            for index in range(1, len(Datas)):
                '''
                获取项目信息
                '''
                projectbaseitem = ProjectBaseItem()
                projectbaseitem['SourceUrl'] = response.url
                Data = Datas[index]
                Projecthref = urlparse.urljoin(
                    main_url, Data.xpath('./td[1]/a/@href').extract_first())

                nPos = str(Projecthref).index('SPJ_ID=')
                projectstr = str(Projecthref)[nPos:]
                projectbaseitem['project_no'] = projectstr.replace(
                    "SPJ_ID=", "")

                ProjectName = Data.xpath('./td[1]/a/text()').extract_first()
                if ProjectName:
                    projectbaseitem['project_name'] = ProjectName
                else:
                    projectbaseitem['project_name'] = ''

                # //*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[2]/td[2]
                project_com_name = Data.xpath('./td[2]/text()').extract_first()
                if project_com_name:
                    projectbaseitem['project_com_name'] = project_com_name
                project_area = Data.xpath('./td[3]/text()').extract_first()
                if project_area:
                    projectbaseitem['project_area'] = project_area
                else:
                    projectbaseitem['project_area'] = ''

                result.append(Request(url=Projecthref,
                                      method='GET',
                                      headers=headers,
                                      meta={
                                          'PageType': 'BuidingPageBase',
                                          'item': projectbaseitem,
                                      }))
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


'''
获取楼栋信息
'''


class BuildingHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        def get_total_page(string):
            total_page = ''
            total_num = ''
            try:

                search_result = re.search(r'共&amp;nbsp(.*?)&amp;nbsp条&amp;nbsp--&amp;nbsp第&amp;nbsp(.*?)&amp;nbsp页&amp;nbsp--&amp;nbsp共&amp;nbsp(.*?)&amp;nbsp页',
                                          str(string))
                if search_result:
                    total_num = search_result.group(1)
                    total_page = search_result.group(3)

            except Exception:
                traceback.print_exc()
            return total_num, total_page
        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('BuidingPageBase'):
            if result:
                return result
            return []

        if response.request.method == 'GET':
            headers = {

                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Host': 'www.szfcweb.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': response.url,
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36'

            }
            page_body = Selector(response).xpath(
                '//*[@id="aspnetForm"]/div[3]/table/tr[2]/td/table').extract_first()
            total_num, page_count = get_total_page(page_body)
            projectitem = response.meta.get('item')
            projectbaseitem = copy.deepcopy(projectitem)
            projectbaseitem['project_building_num'] = total_num
            # //*[@id="ctl00_MainContent_lb_Pro_Add"]
            project_addr = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_lb_Pro_Add"]/text()').extract_first()
            projectbaseitem['project_addr'] = project_addr
            VIEWSTATE = Selector(response).xpath(
                '//*[@id="__VIEWSTATE"]/@value').extract_first()
            VIEWSTATEGENERATOR = Selector(response).xpath(
                '//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
            EVENTVALIDATION = Selector(response).xpath(
                '//*[@id="__EVENTVALIDATION"]/@value').extract_first()
            EVENTARGUMENT = Selector(response).xpath(
                '//*[@id="__EVENTARGUMENT"]/@value').extract_first()
            LASTFOCUS = Selector(response).xpath(
                '//*[@id="__LASTFOCUS"]/@value').extract_first()
            result.append(projectbaseitem)

            req_dict = {
                '__EVENTTARGET': 'ctl00$MainContent$OraclePager1$ctl12$PageList',
                '__VIEWSTATE': VIEWSTATE,
                '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
                '__EVENTVALIDATION': EVENTVALIDATION,
                '__EVENTARGUMENT': EVENTARGUMENT,
                '__LASTFOCUS': LASTFOCUS,
            }
            if page_count:
                if int(page_count) > 1:
                    for page in range(0, int(page_count)):
                        req_dict[
                            'ctl00$MainContent$OraclePager1$ctl12$PageList'] = page
                        req_body = urlparse.urlencode(req_dict)
                        result.append(Request(url=response.url,
                                              body=req_body,
                                              method='POST',
                                              headers=headers,
                                              meta={
                                                  'PageType': 'BuidingPageBase',
                                                  'project_name': projectbaseitem['project_name'],
                                                  'project_area': projectbaseitem['project_area']
                                              }))
                else:
                    req_dict['ctl00$MainContent$OraclePager1$ctl12$PageList'] = 0
                    req_body = urlparse.urlencode(req_dict)
                    result.append(Request(url=response.url,
                                          body=req_body,
                                          method='POST',
                                          headers=headers,
                                          meta={
                                              'PageType': 'BuidingPageBase',
                                              'project_name': projectbaseitem['project_name'],
                                              'project_area': projectbaseitem['project_area']
                                          }))

        elif response.request.method == 'POST':

            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Host': 'www.szfcweb.com',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36'

            }
            nPos = str(response.url).index('SaleInfo')

            main_url = str(response.url)[0:nPos]
            recbuilding = []
            # //*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[2]/td[1]
            Datas = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_OraclePager1"]/tr')
            for index in range(1, len(Datas)):
                buildingbaseitem = BuildingBaseItem()
                buildingbaseitem['SourceUrl'] = response.url
                project_name = response.meta.get('project_name')
                buildingbaseitem['project_name'] = project_name
                project_area = response.meta.get('project_area')
                buildingbaseitem['project_area'] = project_area

                '''
                获取楼栋信息
                '''
                nPos = str(response.url).index('SPJ_ID=')
                projectstr = str(response.url)[nPos:]
                buildingbaseitem['project_no'] = projectstr.replace(
                    "SPJ_ID=", "")

                Buildinghref = urlparse.urljoin(
                    main_url, Datas[index].xpath('./td[1]/a/@href').extract_first())
                buildingbaseitem['building_no'] = re.search(r'PBTAB_ID=(.*?)&SPJ_ID',
                                                            Buildinghref).group(1)
                BuildingName = Datas[index].xpath(
                    './td[1]/a/text()').extract_first()
                while BuildingName in recbuilding:
                    BuildingName = BuildingName + '+1'
                recbuilding.append(BuildingName)
                buildingbaseitem['building_name'] = BuildingName
                building_areas = Datas[index].xpath(
                    './td[2]/text()').extract_first()
                buildingbaseitem['building_areas'] = building_areas
                building_house_num = Datas[index].xpath(
                    './td[3]/text()').extract_first()
                buildingbaseitem['building_house_num'] = building_house_num
                building_total_floor = Datas[index].xpath(
                    './td[4]/text()').extract_first()
                buildingbaseitem['building_total_floor'] = building_total_floor
                result.append(buildingbaseitem)
                # getnum = random.randint(0, 9)
                # getkey = str(self.r.get('SuzhouCrawlerkey%d' % getnum)).replace("b'", "").replace("'", "")
                # headers['Referer'] = re.sub(r'\(S\((.*?)\)\)', getkey, str(response.url))
                # nexturl = re.sub(r'\(S\((.*?)\)\)', getkey, str(Buildinghref))

                # result.append(Request(url=nexturl,
                #                       method='GET',
                #                       headers=headers,
                #                       meta={
                #                           'PageType': 'HouseBase',
                #                           'BuildingName': BuildingName,
                #                           'project_name': project_name,
                #                           'retrytimes': 0
                #                       }))

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return

'''
获取房屋信息
'''


class HouseHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Host': 'www.szfcweb.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36'
        }
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):

        def get_house_state(string):
            STATE_TAB = {
                'background-color:#cccccc;': '不可售',
                'background-color:#66cc33;': '可售',
                'background-color:#666600;': '限制中',
                'background-color:Yellow;': '签约中',
            }
            state = ''
            for key in STATE_TAB:
                if key in string:
                    state = STATE_TAB[key]
                    break
            return state
        result = list(result)
        if not(200 <= response.status < 300):  # common case
            if result:
                return result
            return []
        if response.meta.get('PageType') not in ('HouseBase'):
            if result:
                return result
            return []
        if response.meta.get('PageType') == 'HouseBase':
            Datas1 = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_gvxml"]/tr')
            Datas2 = Selector(response).xpath(
                '//*[@id="ctl00_MainContent_GridView1"]/tr')

            isgetdata = len(Datas1) + len(Datas2)
            BuildingName = response.meta.get('BuildingName')
            project_name = response.meta.get('project_name')
            recordnum = 0
            if int(response.meta.get("retrytimes")) > 20:
                return []
            if isgetdata == 0:
                getnum = random.randint(0, 9)
                getkey = str(self.r.get('SuzhouCrawlerkey%d' %
                                        getnum)).replace("b'", "").replace("'", "")
                self.headers['Referer'] = re.sub(
                    r'\(S\((.*?)\)\)', getkey, str(response.url))
                nexturl = re.sub(r'\(S\((.*?)\)\)', getkey, str(response.url))
                retrytimes = int(response.meta.get('retrytimes')) + 1
                result.append(Request(url=nexturl,
                                      method='GET',
                                      headers=self.headers,
                                      meta={
                                          'PageType': 'HouseBase',
                                          'BuildingName': BuildingName,
                                          'project_name': project_name,
                                          'retrytimes': retrytimes
                                      }))
            else:
                if len(Datas1) == 0:
                    for Data in Datas2:
                        house_infos = Data.xpath('./td')
                        for house_info in house_infos:
                            houseitem = HouseBaseItem()
                            houseitem['SourceUrl'] = response.url
                            house_name = house_info.xpath(
                                './text()').extract_first().strip()
                            if house_name != "":
                                nPos = str(response.url).index('SPJ_ID=')
                                projectstr = str(response.url)[nPos:]
                                project_no = projectstr.replace("SPJ_ID=", "")
                                reserresult = re.search(r'PBTAB_ID=(.*?)&SPJ_ID=',
                                                        str(response.url))
                                bilding_no = reserresult.group(1)
                                houseitem['building_name'] = BuildingName
                                houseitem['project_name'] = project_name
                                houseitem['project_no'] = project_no
                                houseitem['building_no'] = bilding_no
                                houseitem['house_name'] = house_name
                                house_color = house_info.xpath(
                                    './@style').extract_first()

                                house_sts = get_house_state(house_color)
                                houseitem['house_sts'] = house_sts

                                houseitem['house_no'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                   str(project_no) + '|' + str(
                                                                       BuildingName) + '|' + str(
                                                                       house_name) + '|' + str(
                                                                       recordnum)).hex
                                recordnum = recordnum + 1
                                if house_sts == '可售':
                                    q_object = HouseBaseSuzhou.objects
                                    res_object = q_object.filter(house_no=houseitem['house_no']).latest(
                                        field_name='CurTimeStamp')
                                    if not res_object:
                                        getnum = random.randint(0, 9)
                                        getkey = str(self.r.get('SuzhouCrawlerkey%d' % getnum)).replace("b'",
                                                                                                        "").replace(
                                            "'", "")
                                        self.headers['Referer'] = re.sub(
                                            r'\(S\((.*?)\)\)', getkey, str(response.url))
                                        houseinfohref = 'http://spf.szfcweb.com/szfcweb/(S(*))/DataSerach/SaleInfoHouseView.aspx\?' + re.search(
                                            r"SaleInfoHouseView.aspx\?(.*?)'",
                                            str(house_info.xpath('.').extract_first())).group(1)
                                        nexturl = re.sub(
                                            r'\(S\((.*?)\)\)', getkey, str(houseinfohref))
                                        result.append(Request(url=nexturl,
                                                              method='GET',
                                                              headers=self.headers,
                                                              meta={
                                                                  'PageType': 'HouseInfo',
                                                                  'item': houseitem
                                                              }))
                                    else:
                                        result.append(houseitem)

                                else:
                                    result.append(houseitem)

                else:
                    for Data in Datas1:
                        house_infos = Data.xpath('./td')
                        for house_info in house_infos:
                            house_name = house_info.xpath(
                                './text()').extract_first().strip()
                            if house_name != "":
                                houseitem = HouseBaseItem()
                                houseitem['SourceUrl'] = response.url
                                nPos = str(response.url).index('SPJ_ID=')
                                projectstr = str(response.url)[nPos:]
                                project_no = projectstr.replace("SPJ_ID=", "")
                                reserresult = re.search(r'PBTAB_ID=(.*?)&SPJ_ID=',
                                                        str(response.url))
                                bilding_no = reserresult.group(1)
                                houseitem['building_name'] = BuildingName
                                houseitem['project_name'] = project_name
                                houseitem['project_no'] = project_no
                                houseitem['building_no'] = bilding_no
                                houseitem['house_name'] = house_name
                                house_color = house_info.xpath(
                                    './@style').extract_first()
                                house_sts = get_house_state(house_color)
                                houseitem['house_sts'] = house_sts
                                houseitem['house_no'] = uuid.uuid3(uuid.NAMESPACE_DNS,
                                                                   str(project_no) + '|' + str(
                                                                       BuildingName) + '|' + str(
                                                                       house_name) + '|' + str(
                                                                       recordnum)).hex
                                recordnum = recordnum + 1
                                if house_sts == '可售':
                                    q_object = HouseBase.objects
                                    res_object = q_object.filter(house_no=houseitem['house_no']).latest(
                                        field_name='CurTimeStamp')
                                    if not res_object:
                                        getnum = random.randint(0, 9)
                                        getkey = str(self.r.get('SuzhouCrawlerkey%d' % getnum))\
                                            .replace("b'", "").replace("'", "")
                                        self.headers['Referer'] = re.sub(
                                            r'\(S\((.*?)\)\)', getkey, str(response.url))
                                        houseinfohref = 'http://spf.szfcweb.com/szfcweb/(S(*))/DataSerach/SaleInfoHouseView.aspx\?' + re.search(
                                            r"SaleInfoHouseView.aspx\?(.*?)'",
                                            str(house_info.xpath('.').extract_first())).group(1)
                                        nexturl = re.sub(
                                            r'\(S\((.*?)\)\)', getkey, str(houseinfohref))
                                        result.append(Request(url=nexturl,
                                                              method='GET',
                                                              headers=self.headers,
                                                              meta={
                                                                  'PageType': 'HouseInfo',
                                                                  'item': houseitem
                                                              }))
                                    else:
                                        result.append(houseitem)
                                else:
                                    result.append(houseitem)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
'''
获取房屋详细信息
'''


class HouseInfoHandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Host': 'www.szfcweb.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36'
        }
        self.r = redis.Redis(host=setting.REDIS_HOST, port=setting.REDIS_PORT)

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
        if response.meta.get('PageType') not in ('HouseInfo'):
            if result:
                return result
            return []
        houseitem = response.meta.get('item')
        house_info_base = copy.deepcopy(houseitem)
        HSE_Located = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_HSE_Located"]/@value').extract_first()
        house_info_base['HSE_Located'] = check_data_str(HSE_Located)

        HSE_LevelCode = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_HSE_LevelCode"]/@value').extract_first()
        house_info_base['HSE_LevelCode'] = check_data_str(HSE_LevelCode)

        Hes_LevelName = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_Hes_LevelName"]/@value').extract_first()
        house_info_base['Hes_LevelName'] = check_data_str(Hes_LevelName)

        Hse_URCode = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_Hse_URCode"]/@value').extract_first()
        house_info_base['Hse_URCode'] = check_data_str(Hse_URCode)

        HSE_CellCode = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_HSE_CellCode"]/@value').extract_first()
        house_info_base['HSE_CellCode'] = check_data_str(HSE_CellCode)

        Hse_Type_Room = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_Hse_Type_Room"]/@value').extract_first()
        house_info_base['Hse_Type_Room'] = check_data_str(Hse_Type_Room)

        Hse_Type_Hall = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_Hse_Type_Hall"]/@value').extract_first()
        house_info_base['Hse_Type_Hall'] = check_data_str(Hse_Type_Hall)
        HSE_Bathroom = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_HSE_Bathroom"]/@value').extract_first()
        house_info_base['HSE_Bathroom'] = check_data_str(HSE_Bathroom)
        SHSE_ISPOLICY = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_SHSE_ISPOLICY"]/@value').extract_first()
        house_info_base['SHSE_ISPOLICY'] = check_data_str(SHSE_ISPOLICY)
        Hse_Class = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_Hse_Class"]/@value').extract_first()
        house_info_base['Hse_Class'] = check_data_str(Hse_Class)
        PH_Cdate = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_lb_PH_Cdate"]/text()').extract_first()
        house_info_base['PH_Cdate'] = check_data_str(PH_Cdate)
        HSE_Ownership = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_HSE_Ownership"]/@value').extract_first()
        # 土地分割转让许可证编号
        house_info_base['HSE_Ownership'] = check_data_str(HSE_Ownership)
        HSE_LDTPermit_SN = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_HSE_LDTPermit_SN"]/@value').extract_first()
        house_info_base['HSE_LDTPermit_SN'] = check_data_str(HSE_LDTPermit_SN)
        # 抵押情况
        ddl_ProType = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_ddl_ProType"]/option')
        for hse in ddl_ProType:
            if 'selected' in str(hse.xpath('.').extract_first()):
                ddl_ProTypeopt = hse.xpath('./text()').extract_first()
                house_info_base['ddl_ProTypeopt'] = check_data_str(
                    ddl_ProTypeopt)
        # 装修情况
        hf_name = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_hf_name"]/@value').extract_first()
        house_info_base['hf_name'] = check_data_str(hf_name)
        # 抵押起始日期
        lb_ProStar = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_lb_ProStar"]/text()').extract_first()
        house_info_base['lb_ProStar'] = check_data_str(lb_ProStar)
        # 抵押终止日期
        lb_ProEnd = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_lb_ProEnd"]/text()').extract_first()
        house_info_base['lb_ProEnd'] = check_data_str(lb_ProEnd)
        # 套内建筑面积（平方米）
        SFLOOR_IN = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_SFLOOR_IN"]/@value').extract_first()
        house_info_base['SFLOOR_IN'] = check_data_str(SFLOOR_IN)
        # 分摊建筑面积（平方米）
        SFLOOR_FH = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_SFLOOR_FH"]/@value').extract_first()
        house_info_base['SFLOOR_FH'] = check_data_str(SFLOOR_FH)
        # 总建筑面积（平方米）
        AreaAll = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_AreaAll"]/@value').extract_first()
        house_info_base['AreaAll'] = check_data_str(AreaAll)
        # 总价格（元）
        Hse_TSUM = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_Hse_TSUM"]/@value').extract_first()
        house_info_base['Hse_TSUM'] = check_data_str(Hse_TSUM)
        # 单价（元/平方米）
        SFLOOR_PRICE = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_SFLOOR_PRICE"]/@value').extract_first()
        house_info_base['SFLOOR_PRICE'] = check_data_str(SFLOOR_PRICE)
        # 公安门牌号
        Address = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_Address"]/@value').extract_first()
        house_info_base['Address'] = check_data_str(Address)
        # 房屋层高是否超过2.2米
        HSE_IsLevelHeighflag = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_rbt_HSE_IsLevelHeigh_0"]/@value').extract_first()
        if HSE_IsLevelHeighflag == '1':
            HSE_IsLevelHeigh = '是'
        else:
            HSE_IsLevelHeigh = '否'
        house_info_base['HSE_IsLevelHeigh'] = check_data_str(HSE_IsLevelHeigh)

        # 房屋层高（米）
        LevelHeigh = Selector(response).xpath(
            '//*[@id="ctl00_MainContent_txt_LevelHeigh"]/@value').extract_first()
        house_info_base['LevelHeigh'] = check_data_str(LevelHeigh)

        result.append(house_info_base)

        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return


class ProjectBase1HandleMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, settings):
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(crawler.settings)

    def process_spider_output(self, response, result, spider):
        return result

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        return
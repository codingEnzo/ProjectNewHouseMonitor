# coding = utf-8
import functools
import datetime
import pandas as pd
from HouseNew.models import *


def just_one_instance(func):

    @functools.wraps(func)
    def f(*args, **kwargs):
        import socket
        try:
            global s
            s = socket.socket()
            host = socket.gethostname()
            s.bind((host, 60123))
        except Exception:
            print('already has an instance')
            return None
        return func(*args, **kwargs)
    return f


def UpdateProjectAggregateInfo():
    projectCountInfo = ProjectCountInfo()
    df = pd.DataFrame(list(ProjectBase.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
                                         {'$group':
                                             {'_id': "$ProjectUUID",
                                                "ProjectUUID": {'$first': "$ProjectUUID"},
                                                 "SaleNum": {'$first': "$ProjectSaleSum"},
                                             }
                                         }
                                    ])
                            )
                        )
    df['SaleNum'] = df.SaleNum.apply(int)
    amount = df.ProjectUUID.unique().size
    projectCountInfo.ProjectSaledNum = df[df.SaleNum == 0].ProjectUUID.unique().size
    projectCountInfo.ProjectSalingNum = amount - projectCountInfo.ProjectSaledNum
    projectCountInfo.save()


def UpdateBuildingAggregateInfo():
    buildingCountInfo = BuildingCountInfo()
    df_building = pd.DataFrame(list(BuildingInfo.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
                                         {'$group':
                                             {'_id': "$BuildingUUID"}
                                         }
                                    ])
                            )
                        )
    df_house = pd.DataFrame(list(HouseInfo.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
                                         {'$group':
                                             {'_id': "$HouseUUID",
                                                'BuildingUUID': {'$first': "$BuildingUUID"},
                                                'HouseSaleState': {'$first': "$HouseSaleState"}
                                            }
                                         }
                                    ])
                            )
                        )
    amount = df_building.BuildingUUID.unique().size
    buildingCountInfo.BuildingSalingNum = df_house[df_house.HouseSaleState == '可售'].BuildingUUID.unique().size
    buildingCountInfo.BuildingSaledNum = amount - buildingCountInfo.BuildingSalingNum
    buildingCountInfo.save()


def UpdateHousePrice():

    def get_unitprice(subProjectUUID, buildingUUID, houseUUID, houseUsage='', houseTime=str(datetime.datetime.now())):

        def get_project_unitprice(subProjectUUID, houseUsage='', houseTime=str(datetime.datetime.now())):

            def get_saleinfo(source_dict, houseUsage=''):
                result_dict = {}
                houseUsage = str(houseUsage).strip()
                if not isinstance(source_dict, dict):
                    return result_dict
                if not source_dict.get('null'):
                    return result_dict
                if houseUsage == '':
                    return result_dict
                else:
                    if source_dict.get(houseUsage):
                        if isinstance(source_dict.get(houseUsage), dict):
                            info_dict = source_dict.get(houseUsage)
                            if '已签约套数' in info_dict and '已签约面积' in info_dict and '成交均价' in info_dict:
                                result_dict = info_dict
                    else:
                        for key in source_dict:
                            if houseUsage in key:
                                if isinstance(source_dict.get(key), dict):
                                    info_dict = source_dict.get(key)
                                    if '已签约套数' in info_dict and '已签约面积' in info_dict and '成交均价' in info_dict:
                                        result_dict = info_dict
                                        break
                return result_dict

            result = None
            timebase = datetime.datetime.strptime(houseTime, "%Y-%m-%d %H:%M:%S.%f")
            time_lowbound = str(timebase - datetime.timedelta(days=1))
            time_upbound = str(timebase + datetime.timedelta(days=1))
            cur_info = ProjectInfo.objects.filter(SubProjectUUID=subProjectUUID,
                                                    CurTimeStamp__lt=time_upbound,
                                                    CurTimeStamp__gt=time_lowbound).\
                            latest('CurTimeStamp') or\
                        ProjectInfo.objects.filter(SubProjectUUID=subProjectUUID).\
                            latest('CurTimeStamp')
            if cur_info:
                last_info = ProjectInfo.objects.filter(SubProjectUUID=subProjectUUID).\
                                filter(CurTimeStamp__lt=cur_info.CurTimeStamp).latest('CurTimeStamp')
                if last_info:
                    cur_info_dict = get_saleinfo(cur_info.ProjectSaleSum, houseUsage)
                    last_info_dict = get_saleinfo(last_info.ProjectSaleSum, houseUsage)
                    if cur_info_dict == {} or last_info_dict == {}:
                        return result
                    cur_sum_price = cur_info_dict['成交均价'] * cur_info_dict['已签约面积']
                    last_sum_price = last_info_dict['成交均价'] * last_info_dict['已签约面积']
                    area_diff = cur_info_dict['已签约面积'] - last_info_dict['已签约面积']
                    print(area_diff)
                    if area_diff == 0:
                        cur_unit_price = cur_info_dict['成交均价']
                    else:
                        cur_unit_price = (cur_sum_price - last_sum_price) / area_diff
                    if cur_unit_price < 0:
                        return result
                    result = cur_unit_price
                else:
                    cur_info_dict = get_saleinfo(cur_info.ProjectSaleSum, houseUsage)
                    if cur_info_dict == {}:
                        return result
                    cur_unit_price = cur_info_dict['成交均价']
                    if cur_unit_price < 0:
                        return result
                    result = cur_unit_price
            return result

        def get_building_unitprice(buildingUUID):
            result = None
            building_info = BuildingInfo.objects.filter(BuildingUUID=buildingUUID).latest('CurTimeStamp')
            if building_info:
                cur_unit_price = building_info.BuildingSalePrice
                if cur_unit_price:
                    try:
                        result = float(cur_unit_price)
                    except Exception:
                        pass
            return result

        def get_house_unitprice(houseUUID):
            result = None
            house_info = HouseInfo.objects.filter(HouseUUID=houseUUID).latest('CurTimeStamp')
            if house_info:
                cur_unit_price = house_info.HouseBuildingUnitPrice
                if cur_unit_price:
                    try:
                        result = float(cur_unit_price)
                    except Exception:
                        pass
            return result

        unit_price = 0.0
        unit_price_list = [get_project_unitprice(subProjectUUID, houseUsage, houseTime),
                            get_building_unitprice(buildingUUID),
                            get_house_unitprice(houseUUID)]
        for price in unit_price_list:
            if price:
                try:
                    unit_price = float(price)
                    break
                except Exception:
                    pass
        print(unit_price)
        return unit_price

    def fill_bank_field(houseObject):
            field_list = ['HouseUsage',
                'HouseStructure',
                'HouseBuildingArea',
                'HouseInnerArea',
                'HouseBuildingUnitPrice',
                'HouseInnerUnitPrice']
            houseObjectBase = HouseInfo.objects.filter(HouseUUID=houseObject.HouseUUID).\
                                filter(HouseBuildingArea__ne=0.0).latest('CurTimeStamp')
            if houseObjectBase:
                for field in field_list:
                    setattr(houseObject, field, getattr(houseObjectBase, field))
            return houseObject

    house_update_list = HouseInfo.objects.filter(HousePriceFlag=False).all()
    for house in house_update_list:
        house.HouseUnitPrice = get_unitprice(house.SubProjectUUID,
                                                house.BuildingUUID,
                                                house.HouseUUID,
                                                houseUsage=house.HouseUsage,
                                                houseTime=house.CurTimeStamp)
        if house.HouseBuildingArea == 0.0:
            house = fill_bank_field(house)
        house.HousePrice = house.HouseUnitPrice * house.HouseBuildingArea
        house.HousePriceFlag = True
        house.save()


def UpdateHouseAggregateInfo():

    def safe_format(string):
        try:
            string = string.strip()
        except Exception:
            pass
        return string

    houseCountInfo = HouseCountInfo()
    df = pd.DataFrame(list(HouseInfo.objects.aggregate(*[{"$sort": {"CurTimeStamp": -1}},
                                         {'$group':
                                             {'_id': "$HouseUUID",
                                                 "State": {'$first': "$HouseState"},
                                                 "SubState": {'$first': "$HouseSubState"},
                                             }
                                         }
                                    ])
                            )
                        )
    df = df[df.State != '']
    df['State'] = df.State.apply(safe_format)                                            
    df['SubState'] = df.SubState.apply(safe_format)                                            
    gb_dict = df.groupby([df.State, df.SubState])
    houseCountInfo.HouseUnavailableNum = {'dafault': int(gb_dict.get_group(('不可售', '')).size),
                                            'pledged': int(gb_dict.get_group(('不可售', '已办理预售项目抵押')).size)}
    houseCountInfo.HouseAvailableNum = {'dafault': int(gb_dict.get_group(('可售', '')).size),
                                            'pledged': int(gb_dict.get_group(('可售', '已办理预售项目抵押')).size)}
    try:
        houseCountInfo.HouseContractNum = {'dafault': int(gb_dict.get_group(('已签约', '')).size),
                                            'pledged': int(gb_dict.get_group(('已签约', '已办理预售项目抵押')).size)}
    except Exception:
        houseCountInfo.HouseContractNum = {'dafault': int(gb_dict.get_group(('已签约', '')).size),
                                            'pledged': 0}
    houseCountInfo.HouseReserveNum = {'dafault': int(gb_dict.get_group(('已预订', '')).size),
                                            'pledged': int(gb_dict.get_group(('已预订', '已办理预售项目抵押')).size)}
    houseCountInfo.HouseRecordNum = {'dafault': int(gb_dict.get_group(('网上联机备案', '')).size),
                                            'pledged': int(gb_dict.get_group(('网上联机备案', '已办理预售项目抵押')).size)}
    houseCountInfo.HouseAuditNum = {'dafault': int(gb_dict.get_group(('资格核验中', '')).size),
                                            'pledged': int(gb_dict.get_group(('资格核验中', '已办理预售项目抵押')).size)}
    print(houseCountInfo.HouseUnavailableNum)
    print(houseCountInfo.HouseAvailableNum)
    print(houseCountInfo.HouseReserveNum)
    print(houseCountInfo.HouseContractNum)
    print(houseCountInfo.HouseRecordNum)
    print(houseCountInfo.HouseAuditNum)
    houseCountInfo.save()


def run():
    UpdateProjectAggregateInfo()
    UpdateBuildingAggregateInfo()
    UpdateHousePrice()
    UpdateHouseAggregateInfo()

# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseQingdao(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectID = fields.StringField(
        default='', max_length=100, index=True, null=False)  # 项目id
    DistrictName = fields.StringField(
        default='', max_length=50, null=False)  # 行政区
    ProjectName = fields.StringField(
        default='', max_length=100, null=False)  # 楼盘名称
    ProjectAddress = fields.StringField(
        default='', max_length=100, null=False)  # 楼盘地址
    Developer = fields.StringField(
        default='', max_length=100, null=False)  # 开发商
    OnSaleState = fields.StringField(
        default='', max_length=20, null=False)  # 销售状态
    HousingAmount = fields.StringField(
        default='', max_length=100, null=False)  # 住宅套数
    HousingArea = fields.StringField(
        default='', max_length=100, null=False)  # 住宅面积
    TotalAmount = fields.StringField(
        default='', max_length=100, null=False)  # 总套数
    TotalArea = fields.StringField(
        default='', max_length=100, null=False)  # 总面积
    HousingOnsoldAmount = fields.StringField(
        default='', max_length=100, null=False)  # 可售住宅套数
    HousingOnsoldArea = fields.StringField(
        default='', max_length=100, null=False)  # 可售住宅面积
    TotalOnsoldAmount = fields.StringField(
        default='', max_length=100, null=False)  # 可售总套数
    TotalOnsoldArea = fields.StringField(
        default='', max_length=100, null=False)  # 可售总面积
    BookingHousingAmount = fields.StringField(
        default='', max_length=100, null=False)  # 预定住宅套数
    BookingHousingArea = fields.StringField(
        default='', max_length=100, null=False)  # 预定住宅面积
    TotalBookingAmount = fields.StringField(
        default='', max_length=100, null=False)  # 预定总套数
    TotalBookingArea = fields.StringField(
        default='', max_length=100, null=False)  # 预定总面积
    HousingSoldAmount = fields.StringField(
        default='', max_length=100, null=False)  # 已售住宅套数
    HousingSoldArea = fields.StringField(
        default='', max_length=100, null=False)  # 已售住宅面积
    TotalSoldAmount = fields.StringField(
        default='', max_length=100, null=False)  # 已售总套数
    TotalSoldArea = fields.StringField(
        default='', max_length=100, null=False)  # 已售总面积
    RegisterHousingAmount = fields.StringField(
        default='', max_length=100, null=False)  # 已登记住宅套数
    RegisterHousingArea = fields.StringField(
        default='', max_length=100, null=False)  # 已登记住宅面积
    TotalRegisterAmount = fields.StringField(
        default='', max_length=100, null=False)  # 已登记总套数
    TotalRegisterArea = fields.StringField(
        default='', max_length=100, null=False)  # 已登记总面积
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectID',
            'DistrictName',
            'ProjectName',
            'OnSaleState',
            'HousingAmount',
            'HousingArea',
            'TotalAmount',
            'TotalArea',
        ]
    }


class PresellInfoQingdao(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellID = fields.StringField(
        default='', index=True, max_length=100, null=False)  # 预售证id
    ProjectName = fields.StringField(
        default='', max_length=100, null=False)  # 楼盘名称
    PresalePermitNumber = fields.StringField(
        default='', max_length=100, null=False)  # 预售证编号
    PresalePermitName = fields.StringField(
        default='', max_length=100, null=False)  # 预售许可证
    EarliestOpeningDate = fields.StringField(
        default='', max_length=100, null=False)  # 开盘日期
    SellAddress = fields.StringField(
        default='', max_length=200, null=False)  # 售楼地址
    SellTel = fields.StringField(
        default='', max_length=100, null=False)  # 售楼电话
    TotalAmount = fields.StringField(
        default='', max_length=100, null=False)  # 总套数
    TotalArea = fields.StringField(
        default='', max_length=100, null=False)  # 总面积
    OnsoldAmount = fields.StringField(
        default='', max_length=100, null=False)  # 可售总套数
    OnsoldArea = fields.StringField(
        default='', max_length=100, null=False)  # 可售总面积
    SoldAmount = fields.StringField(
        default='', max_length=100, null=False)  # 已售总套数
    SoldArea = fields.StringField(
        default='', max_length=100, null=False)  # 已售总面积
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'PresellID',
            'ProjectName',
            'PresalePermitNumber',
            'PresalePermitName',
            'TotalAmount',
            'TotalArea',
            'OnsoldAmount',
            'OnsoldArea',
            'SoldAmount',
            'SoldArea',
        ]
    }


class BuildingInfoQingdao(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(
        default='', max_length=100, null=False)  # 楼盘名称
    PresalePermitName = fields.StringField(
        default='', max_length=100, null=False)  # 预售许可证
    BuildingID = fields.StringField(
        default='', max_length=100, index=True, null=False)  # 楼栋id
    BuildingName = fields.StringField(default='', max_length=100)  # 楼栋名
    BuildingReferencePrice = fields.StringField(
        default='', max_length=100)  # 参考价格
    BuildingFloatingRange = fields.StringField(
        default='', max_length=100)  # 可浮动幅度
    OnsoldAmount = fields.StringField(default='', max_length=100)  # 可售套数
    BookingAmount = fields.StringField(default='', max_length=100)  # 预定套数
    TotalAmount = fields.StringField(default='', max_length=100)  # 总套数
    BuildingURL = fields.URLField(
        default=None, null=True, blank=True)  # 一房一价地址
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'BuildingUUID',
            'BuildingID',
            'BuildingURL',
            'ProjectName',
            'PresalePermitName',
            'BuildingName',
        ]
    }


class HouseInfoQingdao(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False,
                                 null=False)  # BuildingUUID+实际层+在页面上的列数 生成唯一id
    ProjectName = fields.StringField(
        default='', max_length=100, null=False)  # 楼盘名称
    PresalePermitName = fields.StringField(
        default='', max_length=100, null=False)  # 预售许可证
    BuildingName = fields.StringField(default='', max_length=100)  # 楼栋名
    HouseID = fields.StringField(
        default='', max_length=100, index=True, null=False)  # 房间id
    FloorName = fields.StringField(
        default='', max_length=100, null=False)  # 名义层
    ActualFloor = fields.StringField(
        default='', max_length=100, null=False)  # 实际层
    HouseName = fields.StringField(
        default='', max_length=100, index=True)  # 房间号
    HouseUseType = fields.StringField(default='', max_length=100)  # 房屋类型
    HouseUnitShape = fields.StringField(default='', max_length=100)  # 房型
    ForecastBuildingArea = fields.StringField(default='')  # 预测面积
    MeasuredBuildingArea = fields.StringField(default='')  # 实测面积
    ForecastInsideOfBuildingArea = fields.StringField(default='')  # 预测套内面积
    MeasuredInsideOfBuildingArea = fields.StringField(default='')  # 实测套内面积
    ForecastPublicArea = fields.StringField(default='')  # 预测分摊面积
    MeasuredSharedPublicArea = fields.StringField(default='')  # 实测分摊面积
    ForecastUndergroundArea = fields.StringField(default='')  # 预测地下面积
    MeasuredUndergroundArea = fields.StringField(default='')  # 实测地下面积
    HouseReferencePrice = fields.StringField(default='')  # 参考价格
    HouseState = fields.StringField(
        default='', max_length=100, null=False)  # 状态
    HouseStateLatest = fields.StringField(default='', max_length=255)  # 上次状态
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 户详情地址
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'BuildingUUID',
            'HouseUUID',
            'SourceUrl',
            'ProjectName',
            'PresalePermitName',
            'BuildingName',
            'HouseName',
            'HouseUseType',
            'HouseState',
            'HouseStateLatest',
            'HouseUnitShape',
        ]
    }

# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectInfoGuangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectID = fields.StringField(default='', null=False, max_length=255)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    PresalePermitNumber = fields.StringField(default='', max_length=255)  # 预售证
    ProjectAddress = fields.StringField(default='', max_length=255)
    Developer = fields.StringField(default='', max_length=255)
    DistrictName = fields.StringField(default='', max_length=255)  # 行政区
    RegionName = fields.StringField(default='', max_length=255)  # 片区
    FloorArea = fields.StringField(default='', max_length=255)  # 占地面积
    TotalBuildingArea = fields.StringField(default='', max_length=255)  # 建筑面积
    QualificationNumber = fields.StringField(default='', max_length=255)
    HouseUseType = fields.StringField(default='', max_length=255)
    CertificateOfUseOfStateOwnedLand = fields.StringField(default='')  # 国土证
    ConstructionPermitNumber = fields.StringField(default='')  # 施工许可证
    BuildingPermit = fields.StringField(default='')  # 规划许可证
    ApprovalPresaleAmount = fields.StringField(default='', max_length=255)
    ApprovalPresaleArea = fields.StringField(default='', max_length=255)
    TotalSoldAmount = fields.StringField(default='', max_length=255)  # 已售总套数
    TotalSoldArea = fields.StringField(default='', max_length=255)  # 已售总套数
    TotalUnsoldAmount = fields.StringField(default='', max_length=255)  # 未售总套数
    TotalUnsoldArea = fields.StringField(default='', max_length=255)  # 未售总面积
    HousingTotalSoldAmount = fields.StringField(
        default='', max_length=255)  # 住宅累计已售套数
    HousingTotalSoldArea = fields.StringField(
        default='', max_length=255)  # 住宅累计已售面积
    HousingTotalSoldPrice = fields.StringField(
        default='', max_length=255)  # 住宅累计已售均价
    HousingUnsoldAmount = fields.StringField(
        default='', max_length=255)  # 住宅未售套数
    HousinglUnsoldArea = fields.StringField(
        default='', max_length=255)  # 住宅未售面积
    ShopTotalSoldAmount = fields.StringField(
        default='', max_length=255)  # 商业累计已售套数
    ShopTotalSoldArea = fields.StringField(
        default='', max_length=255)  # 商业累计已售面积
    ShopTotalSoldPrice = fields.StringField(
        default='', max_length=255)  # 商业累计已售均价
    ShopUnsoldAmount = fields.StringField(default='', max_length=255)  # 商业未售套数
    ShoplUnsoldArea = fields.StringField(default='', max_length=255)  # 商业未售面积
    OfficeTotalSoldAmount = fields.StringField(
        default='', max_length=255)  # 办公累计已售套数
    OfficeTotalSoldArea = fields.StringField(
        default='', max_length=255)  # 办公累计已售面积
    OfficeTotalSoldPrice = fields.StringField(
        default='', max_length=255)  # 办公累计已售均价
    OfficeUnsoldAmount = fields.StringField(
        default='', max_length=255)  # 办公未售套数
    OfficelUnsoldArea = fields.StringField(
        default='', max_length=255)  # 办公未售面积
    ParkingTotalSoldAmount = fields.StringField(
        default='', max_length=255)  # 车位累计已售套数
    ParkingTotalSoldArea = fields.StringField(
        default='', max_length=255)  # 车位累计已售面积
    ParkingTotalSoldPrice = fields.StringField(
        default='', max_length=255)  # 车位累计已售均价
    ParkingUnsoldAmount = fields.StringField(
        default='', max_length=255)  # 车位未售套数
    ParkinglUnsoldArea = fields.StringField(
        default='', max_length=255)  # 车位未售面积
    OtherTotalSoldAmount = fields.StringField(
        default='', max_length=255)  # 其他累计已售套数
    OtherTotalSoldArea = fields.StringField(
        default='', max_length=255)  # 其他累计已售面积
    OtherTotalSoldPrice = fields.StringField(
        default='', max_length=255)  # 其他累计已售均价
    OtherUnsoldAmount = fields.StringField(
        default='', max_length=255)  # 其他未售套数
    OtherlUnsoldArea = fields.StringField(default='', max_length=255)  # 其他未售面积
    HousingSoldAmount = fields.StringField(
        default='', max_length=255)  # 住宅当日已售套数
    HousingSoldArea = fields.StringField(
        default='', max_length=255)  # 住宅当日已售面积
    HousingCheckoutAmount = fields.StringField(
        default='', max_length=255)  # 住宅当日退房套数
    ShopSoldAmount = fields.StringField(default='', max_length=255)  # 商业当日已售套数
    ShopSoldArea = fields.StringField(default='', max_length=255)  # 商业当日已售面积
    ShopCheckoutAmount = fields.StringField(
        default='', max_length=255)  # 商业当日退房套数
    OfficeSoldAmount = fields.StringField(
        default='', max_length=255)  # 办公当日已售套数
    OfficeSoldArea = fields.StringField(default='', max_length=255)  # 办公当日已售面积
    OfficeCheckoutAmount = fields.StringField(
        default='', max_length=255)  # 办公当日退房套数
    ParkingSoldAmount = fields.StringField(
        default='', max_length=255)  # 车位当日已售套数
    ParkingSoldArea = fields.StringField(
        default='', max_length=255)  # 车位当日已售面积
    ParkingCheckoutAmount = fields.StringField(
        default='', max_length=255)  # 车位当日退房套数
    OtherSoldAmount = fields.StringField(
        default='', max_length=255)  # 其他当日已售套数
    OtherSoldArea = fields.StringField(default='', max_length=255)  # 其他当日已售面积
    OtherCheckoutAmount = fields.StringField(
        default='', max_length=255)  # 其他当日退房套数
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 项目详细URL
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectID',
            'ProjectName',
            'PresalePermitNumber',
            'DistrictName',
            'RegionName',
            'ProjectAddress',
            'TotalSoldAmount',
            'TotalUnsoldAmount',
            'SourceUrl',
        ]
    }


class PresellInfoGuangzhou(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellID = fields.StringField(default='', null=False, max_length=255)
    ProjectID = fields.StringField(default='', null=False, max_length=255)
    ProjectName = fields.StringField(default='', max_length=255)
    PresalePermitNumber = fields.StringField(default='', max_length=255)
    PresaleBuildingAmount = fields.StringField(default='', max_length=255)
    ConstructionFloorCount = fields.StringField(default='', max_length=255)
    BuiltFloorCount = fields.StringField(default='', max_length=255)
    PeriodsCount = fields.StringField(default='', max_length=255)
    ConstructionTotalArea = fields.StringField(default='', max_length=255)
    GroundArea = fields.StringField(default='', max_length=255)
    UnderGroundArea = fields.StringField(default='', max_length=255)
    PresaleUnitCount = fields.StringField(default='', max_length=255)
    PresaleTotalBuildingArea = fields.StringField(default='', max_length=255)
    PresaleHousingLandIsMortgage = fields.StringField(
        default='', max_length=255)
    PresaleBuildingSupportingAreaInfo = fields.StringField(
        default='', max_length=255)
    LssueDate = fields.StringField(default='', max_length=255)
    LssuingAuthority = fields.StringField(default='', max_length=255)
    HouseSpread = fields.DictField(default={'null': True})  # 房屋分布
    Contacts = fields.StringField(default='', max_length=255)  # 联系人
    ValidityDateStartDate = fields.StringField(
        default='', max_length=255)  # 有效期自
    ValidityDateClosingDate = fields.StringField(
        default='', max_length=255)  # 有效期至
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'PresellID',
            'PresalePermitNumber',
        ]
    }


class BuildingInfoGuangzhou(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectID = fields.StringField(default='', null=False, max_length=255)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)
    BuildingID = fields.StringField(default='', max_length=255)  # 楼栋id
    BuildingName = fields.StringField(default='', max_length=255)  # 楼栋名
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectID',
            'ProjectUUID',
            'BuildingUUID',
            'BuildingID',
            'BuildingName',
        ]
    }


class HouseInfoGuangzhou(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseID = fields.StringField(default='', max_length=255)  # 户id
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    BuildingName = fields.StringField(default='', max_length=255)  # 楼栋名称
    HouseNumber = fields.StringField(default='', max_length=255)  # 房号
    HouseName = fields.StringField(default='', max_length=255)  # 名义房号
    HouseUseType = fields.StringField(default='', max_length=255)  # 房屋功能/用途
    ActualFloor = fields.StringField(default='', max_length=255)  # 实际层
    FloorName = fields.StringField(default='', max_length=255)  # 名义层
    FloorHight = fields.StringField(default='', max_length=255)  # 层高
    FloorCount = fields.StringField(default='', max_length=255)  # 层数/最高层?
    UnitShape = fields.StringField(default='', max_length=255)  # 户型
    IsPrivateUse = fields.StringField(default='', max_length=255)  # 是否自用
    IsSharedPublicMatching = fields.StringField(
        default='', max_length=255)  # 是否公建配套
    IsMoveBack = fields.StringField(default='', max_length=255)  # 是否回迁
    BuildingStructure = fields.StringField(default='', max_length=255)
    Balconys = fields.StringField(default='', max_length=255)
    UnenclosedBalconys = fields.StringField(default='', max_length=255)
    Kitchens = fields.StringField(default='', max_length=255)  # 阳台数量
    Toilets = fields.StringField(default='', max_length=255)  # 卫生间数量
    ForecastBuildingArea = fields.StringField(
        default='', max_length=255)  # 预测建筑面积
    ForecastInsideOfBuildingArea = fields.StringField(
        default='', max_length=255)  # 预测套内面积
    ForecastPublicArea = fields.StringField(
        default='', max_length=255)  # 预测公摊面积
    MeasuredBuildingArea = fields.StringField(
        default='', max_length=255)  # 实测建筑面积
    MeasuredInsideOfBuildingArea = fields.StringField(
        default='', max_length=255)  # 实测套内面积
    MeasuredSharedPublicArea = fields.StringField(
        default='', max_length=255)  # 实测公摊面积
    IsMortgage = fields.StringField(default='', max_length=255)  # 是否抵押
    IsAttachment = fields.StringField(default='', max_length=255)  # 是否查封
    HouseState = fields.StringField(default='', max_length=255)  # 当前状态
    HouseStateLatest = fields.StringField(default='', max_length=255)  # 上次状态
    HouseLabel = fields.StringField(default='', max_length=255)  # 当前标签
    HouseLabelLatest = fields.StringField(default='', max_length=255)  # 上次标签
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 户详细URL
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'BuildingUUID',
            'BuildingName',
            'HouseUUID',
            'HouseID',
            'HouseNumber',
            'HouseUseType',
            'ForecastBuildingArea',
            'ForecastInsideOfBuildingArea',
            'ForecastPublicArea',
            'MeasuredBuildingArea',
            'MeasuredInsideOfBuildingArea',
            'MeasuredSharedPublicArea',
            'HouseState',
            'HouseStateLatest',
            'HouseLabel',
            'HouseLabelLatest',
            'SourceUrl',
        ]
    }


class PermitInfoGuangzhou(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectID = fields.StringField(default='', null=False, max_length=255)
    PermitUUID = fields.UUIDField(default=uuid.uuid3(
        uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)
    PermitType = fields.StringField(null=False, max_length=255)
    Content = fields.DictField(default={'null': True}, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectID',
            'PermitUUID',
            'ProjectName',
            'PermitType',
        ]
    }

# encoding = utf-8
from HouseNew.HouseNewModels.GuiyangModels import *
from HouseNew.HouseNewModels.TaiyuanModels import *
from HouseNew.HouseNewModels.ChangzhouModels import *
from HouseNew.HouseNewModels.HefeiModels import *
from HouseNew.HouseNewModels.DalianModels import *
from HouseNew.HouseNewModels.DongguanModels import *
from HouseNew.HouseNewModels.ChangshaModels import *
from HouseNew.HouseNewModels.HangzhouModels import *
from HouseNew.HouseNewModels.ChongqingModels import *
from HouseNew.HouseNewModels.NanchangModels import *
from HouseNew.HouseNewModels.NantongModels import *
from HouseNew.HouseNewModels.QuanzhouModels import *
from HouseNew.HouseNewModels.JiujiangModels import *
from HouseNew.HouseNewModels.JinanModels import *
from HouseNew.HouseNewModels.ZhaoqingModels import *
from HouseNew.HouseNewModels.SuzhouModels import *
from HouseNew.HouseNewModels.FuzhouModels import *


class ProjectInfoGuangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
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
    HousingTotalSoldAmount = fields.StringField(default='', max_length=255)  # 住宅累计已售套数
    HousingTotalSoldArea = fields.StringField(default='', max_length=255)  # 住宅累计已售面积
    HousingTotalSoldPrice = fields.StringField(default='', max_length=255)  # 住宅累计已售均价
    HousingUnsoldAmount = fields.StringField(default='', max_length=255)  # 住宅未售套数
    HousinglUnsoldArea = fields.StringField(default='', max_length=255)  # 住宅未售面积
    ShopTotalSoldAmount = fields.StringField(default='', max_length=255)  # 商业累计已售套数
    ShopTotalSoldArea = fields.StringField(default='', max_length=255)  # 商业累计已售面积
    ShopTotalSoldPrice = fields.StringField(default='', max_length=255)  # 商业累计已售均价
    ShopUnsoldAmount = fields.StringField(default='', max_length=255)  # 商业未售套数
    ShoplUnsoldArea = fields.StringField(default='', max_length=255)  # 商业未售面积
    OfficeTotalSoldAmount = fields.StringField(default='', max_length=255)  # 办公累计已售套数
    OfficeTotalSoldArea = fields.StringField(default='', max_length=255)  # 办公累计已售面积
    OfficeTotalSoldPrice = fields.StringField(default='', max_length=255)  # 办公累计已售均价
    OfficeUnsoldAmount = fields.StringField(default='', max_length=255)  # 办公未售套数
    OfficelUnsoldArea = fields.StringField(default='', max_length=255)  # 办公未售面积
    ParkingTotalSoldAmount = fields.StringField(default='', max_length=255)  # 车位累计已售套数
    ParkingTotalSoldArea = fields.StringField(default='', max_length=255)  # 车位累计已售面积
    ParkingTotalSoldPrice = fields.StringField(default='', max_length=255)  # 车位累计已售均价
    ParkingUnsoldAmount = fields.StringField(default='', max_length=255)  # 车位未售套数
    ParkinglUnsoldArea = fields.StringField(default='', max_length=255)  # 车位未售面积
    OtherTotalSoldAmount = fields.StringField(default='', max_length=255)  # 其他累计已售套数
    OtherTotalSoldArea = fields.StringField(default='', max_length=255)  # 其他累计已售面积
    OtherTotalSoldPrice = fields.StringField(default='', max_length=255)  # 其他累计已售均价
    OtherUnsoldAmount = fields.StringField(default='', max_length=255)  # 其他未售套数
    OtherlUnsoldArea = fields.StringField(default='', max_length=255)  # 其他未售面积
    HousingSoldAmount = fields.StringField(default='', max_length=255)  # 住宅当日已售套数
    HousingSoldArea = fields.StringField(default='', max_length=255)  # 住宅当日已售面积
    HousingCheckoutAmount = fields.StringField(default='', max_length=255)  # 住宅当日退房套数
    ShopSoldAmount = fields.StringField(default='', max_length=255)  # 商业当日已售套数
    ShopSoldArea = fields.StringField(default='', max_length=255)  # 商业当日已售面积
    ShopCheckoutAmount = fields.StringField(default='', max_length=255)  # 商业当日退房套数
    OfficeSoldAmount = fields.StringField(default='', max_length=255)  # 办公当日已售套数
    OfficeSoldArea = fields.StringField(default='', max_length=255)  # 办公当日已售面积
    OfficeCheckoutAmount = fields.StringField(default='', max_length=255)  # 办公当日退房套数
    ParkingSoldAmount = fields.StringField(default='', max_length=255)  # 车位当日已售套数
    ParkingSoldArea = fields.StringField(default='', max_length=255)  # 车位当日已售面积
    ParkingCheckoutAmount = fields.StringField(default='', max_length=255)  # 车位当日退房套数
    OtherSoldAmount = fields.StringField(default='', max_length=255)  # 其他当日已售套数
    OtherSoldArea = fields.StringField(default='', max_length=255)  # 其他当日已售面积
    OtherCheckoutAmount = fields.StringField(default='', max_length=255)  # 其他当日退房套数
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
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
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
    PresaleHousingLandIsMortgage = fields.StringField(default='', max_length=255)
    PresaleBuildingSupportingAreaInfo = fields.StringField(default='', max_length=255)
    LssueDate = fields.StringField(default='', max_length=255)
    LssuingAuthority = fields.StringField(default='', max_length=255)
    HouseSpread = fields.DictField(default={'null': True})  # 房屋分布
    Contacts = fields.StringField(default='', max_length=255)  # 联系人
    ValidityDateStartDate = fields.StringField(default='', max_length=255)  # 有效期自
    ValidityDateClosingDate = fields.StringField(default='', max_length=255)  # 有效期至
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
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectID = fields.StringField(default='', null=False, max_length=255)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
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
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
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
    IsSharedPublicMatching = fields.StringField(default='', max_length=255)  # 是否公建配套
    IsMoveBack = fields.StringField(default='', max_length=255)  # 是否回迁
    BuildingStructure = fields.StringField(default='', max_length=255)
    Balconys = fields.StringField(default='', max_length=255)
    UnenclosedBalconys = fields.StringField(default='', max_length=255)
    Kitchens = fields.StringField(default='', max_length=255)  # 阳台数量
    Toilets = fields.StringField(default='', max_length=255)  # 卫生间数量
    ForecastBuildingArea = fields.StringField(default='', max_length=255)  # 预测建筑面积
    ForecastInsideOfBuildingArea = fields.StringField(default='', max_length=255)  # 预测套内面积
    ForecastPublicArea = fields.StringField(default='', max_length=255)  # 预测公摊面积
    MeasuredBuildingArea = fields.StringField(default='', max_length=255)  # 实测建筑面积
    MeasuredInsideOfBuildingArea = fields.StringField(default='', max_length=255)  # 实测套内面积
    MeasuredSharedPublicArea = fields.StringField(default='', max_length=255)  # 实测公摊面积
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
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectID = fields.StringField(default='', null=False, max_length=255)
    PermitUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
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


class ProjectBaseQingdao(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectID = fields.StringField(default='', max_length=100, index=True, null=False)  # 项目id
    DistrictName = fields.StringField(default='', max_length=50, null=False)  # 行政区
    ProjectName = fields.StringField(default='', max_length=100, null=False)  # 楼盘名称
    ProjectAddress = fields.StringField(default='', max_length=100, null=False)  # 楼盘地址
    Developer = fields.StringField(default='', max_length=100, null=False)  # 开发商
    OnSaleState = fields.StringField(default='', max_length=20, null=False)  # 销售状态
    HousingAmount = fields.StringField(default='', max_length=100, null=False)  # 住宅套数
    HousingArea = fields.StringField(default='', max_length=100, null=False)  # 住宅面积
    TotalAmount = fields.StringField(default='', max_length=100, null=False)  # 总套数
    TotalArea = fields.StringField(default='', max_length=100, null=False)  # 总面积
    HousingOnsoldAmount = fields.StringField(default='', max_length=100, null=False)  # 可售住宅套数
    HousingOnsoldArea = fields.StringField(default='', max_length=100, null=False)  # 可售住宅面积
    TotalOnsoldAmount = fields.StringField(default='', max_length=100, null=False)  # 可售总套数
    TotalOnsoldArea = fields.StringField(default='', max_length=100, null=False)  # 可售总面积
    BookingHousingAmount = fields.StringField(default='', max_length=100, null=False)  # 预定住宅套数
    BookingHousingArea = fields.StringField(default='', max_length=100, null=False)  # 预定住宅面积
    TotalBookingAmount = fields.StringField(default='', max_length=100, null=False)  # 预定总套数
    TotalBookingArea = fields.StringField(default='', max_length=100, null=False)  # 预定总面积
    HousingSoldAmount = fields.StringField(default='', max_length=100, null=False)  # 已售住宅套数
    HousingSoldArea = fields.StringField(default='', max_length=100, null=False)  # 已售住宅面积
    TotalSoldAmount = fields.StringField(default='', max_length=100, null=False)  # 已售总套数
    TotalSoldArea = fields.StringField(default='', max_length=100, null=False)  # 已售总面积
    RegisterHousingAmount = fields.StringField(default='', max_length=100, null=False)  # 已登记住宅套数
    RegisterHousingArea = fields.StringField(default='', max_length=100, null=False)  # 已登记住宅面积
    TotalRegisterAmount = fields.StringField(default='', max_length=100, null=False)  # 已登记总套数
    TotalRegisterArea = fields.StringField(default='', max_length=100, null=False)  # 已登记总面积
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
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellID = fields.StringField(default='', index=True, max_length=100, null=False)  # 预售证id
    ProjectName = fields.StringField(default='', max_length=100, null=False)  # 楼盘名称
    PresalePermitNumber = fields.StringField(default='', max_length=100, null=False)  # 预售证编号
    PresalePermitName = fields.StringField(default='', max_length=100, null=False)  # 预售许可证
    EarliestOpeningDate = fields.StringField(default='', max_length=100, null=False)  # 开盘日期
    SellAddress = fields.StringField(default='', max_length=200, null=False)  # 售楼地址
    SellTel = fields.StringField(default='', max_length=100, null=False)  # 售楼电话
    TotalAmount = fields.StringField(default='', max_length=100, null=False)  # 总套数
    TotalArea = fields.StringField(default='', max_length=100, null=False)  # 总面积
    OnsoldAmount = fields.StringField(default='', max_length=100, null=False)  # 可售总套数
    OnsoldArea = fields.StringField(default='', max_length=100, null=False)  # 可售总面积
    SoldAmount = fields.StringField(default='', max_length=100, null=False)  # 已售总套数
    SoldArea = fields.StringField(default='', max_length=100, null=False)  # 已售总面积
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
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=100, null=False)  # 楼盘名称
    PresalePermitName = fields.StringField(default='', max_length=100, null=False)  # 预售许可证
    BuildingID = fields.StringField(default='', max_length=100, index=True, null=False)  # 楼栋id
    BuildingName = fields.StringField(default='', max_length=100)  # 楼栋名
    BuildingReferencePrice = fields.StringField(default='', max_length=100)  # 参考价格
    BuildingFloatingRange = fields.StringField(default='', max_length=100)  # 可浮动幅度
    OnsoldAmount = fields.StringField(default='', max_length=100)  # 可售套数
    BookingAmount = fields.StringField(default='', max_length=100)  # 预定套数
    TotalAmount = fields.StringField(default='', max_length=100)  # 总套数
    BuildingURL = fields.URLField(default=None, null=True, blank=True)  # 一房一价地址
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
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False,
                                 null=False)  # BuildingUUID+实际层+在页面上的列数 生成唯一id
    ProjectName = fields.StringField(default='', max_length=100, null=False)  # 楼盘名称
    PresalePermitName = fields.StringField(default='', max_length=100, null=False)  # 预售许可证
    BuildingName = fields.StringField(default='', max_length=100)  # 楼栋名
    HouseID = fields.StringField(default='', max_length=100, index=True, null=False)  # 房间id
    FloorName = fields.StringField(default='', max_length=100, null=False)  # 名义层
    ActualFloor = fields.StringField(default='', max_length=100, null=False)  # 实际层
    HouseName = fields.StringField(default='', max_length=100, index=True)  # 房间号
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
    HouseState = fields.StringField(default='', max_length=100, null=False)  # 状态
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


class ProjectBaseWulumuqi(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PropertyID = fields.StringField(default='', max_length=100, null=False)  # 楼盘id
    sid = fields.StringField(default='33', max_length=100, null=False)  # sid
    ProjectAllrankvalue = fields.StringField(default='', max_length=100)  # 综合评分
    ProjectName = fields.StringField(default='', max_length=100, null=False)  # 楼盘名称
    PromotionName = fields.StringField(default=None, null=True, blank=True, max_length=50)  # 推广名
    DistrictName = fields.StringField(default='', max_length=50)  # 行政区
    RegionName = fields.StringField(default='', max_length=50)  # 街道
    ProjectAddress = fields.StringField(default='', max_length=100, null=False)  # 楼盘地址
    ProjectSellAddress = fields.StringField(default='', max_length=100)  # 售楼地址
    ProjectMainUnitType = fields.StringField(default='', max_length=100)  # 主力户型
    ProjectDecoration = fields.StringField(default='', max_length=100)  # 装修情况
    BuildingType = fields.StringField(default='', max_length=100)  # 建筑类型/建筑形式
    LandUse = fields.StringField(default='', max_length=100)  # 物业类型/土地用途
    FloorAreaRatio = fields.StringField(default='', max_length=100)  # 容积率
    GreeningRate = fields.StringField(default='', max_length=100)  # 绿化率
    FloorArea = fields.StringField(default='', max_length=100)  # 占地面积
    CompletionDate = fields.StringField(default='', max_length=100)  # 竣工时间
    TotalBuidlingArea = fields.StringField(default='', max_length=100)  # 总建筑面积
    HousingCount = fields.StringField(default='', max_length=100)  # 总户数
    LatestDeliversHouseDate = fields.StringField(default='', max_length=100)  # 预计交付时间
    ParkingInfo = fields.StringField(default='', max_length=100)  # 车位信息
    ManagementFees = fields.StringField(default='', max_length=100)  # 物业费
    ManagementCompany = fields.StringField(default='', max_length=100)  # 物业公司
    PropertyRightsDescription = fields.StringField(default='', max_length=100)  # 产权年限
    Developer = fields.StringField(default='', max_length=100)  # 项目公司
    Selltel = fields.StringField(default='', max_length=100)  # 售楼部电话
    OnSaleState = fields.StringField(default='', max_length=100, null=False)  # 楼盘状态/在售状态
    TrafficSituation = fields.StringField(default='')  # 交通情况
    ProjectSupporting = fields.StringField(default='')  # 项目配套
    ProjectIntro = fields.StringField(default='')  # 项目简介
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 项目详细URL
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
        ]
    }


class PresellInfoWulumuqi(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)  # 创建时间
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellID = fields.StringField(default='', max_length=100, null=False)  # 预售证id
    PropertyID = fields.StringField(default='', max_length=100, null=False)  # 预售证id
    sid = fields.StringField(default='', max_length=100, index=True, null=False)  # sid
    PresellNO = fields.StringField(default='')  # 预售证号/预售证编号
    PresellName = fields.StringField(default='', null=True)  # 预售证号/预售证编号
    LandUse = fields.StringField(default='', max_length=100)  # 物业类型/土地用途
    LssueDate = fields.StringField(default='', max_length=100, null=True)  # 预售证核发时间
    Applycorp = fields.StringField(default='', max_length=100, null=True)  # 预售证申领单位
    LssuingAuthority = fields.StringField(default='', max_length=100, null=True, blank=True)  # 发证机关
    ApprovalPresalePosition = fields.StringField(default='', max_length=100, null=True, blank=True)  # 批准预售位置

    Bank = fields.StringField(default='', max_length=100, null=True, blank=True)  # 资金监管银行
    BankAccount = fields.StringField(default='', max_length=100, null=True)  # 资金监管银行账号
    # 接口返回的字段
    num = fields.IntField(default=0, null=True, blank=True)  # 纳入网上预（销）售总套数
    justnum = fields.IntField(default=0, null=True, blank=True)  # 即将解除限制房产套数
    area = fields.FloatField(default=0.00, null=True, blank=True)  # 纳入网上预（销）售总面积
    justarea = fields.FloatField(default=0.00, null=True, blank=True)  # 即将解除限制房产总面积
    avanum = fields.IntField(default=0, null=True, blank=True)  # 可预（销）售总套数
    waitnum = fields.IntField(default=0, null=True, blank=True)  # 待现售房产套数
    avaarea = fields.FloatField(default=0.00, null=True, blank=True)  # 可预（销）售总面积
    waitarea = fields.FloatField(default=0.00, null=True, blank=True)  # 可预（销）售总套数
    resideavanum = fields.IntField(default=0, null=True, blank=True)  # 其中可预（销）售住宅总套数
    limitnum = fields.IntField(default=0, null=True, blank=True)  # 限制房产套数
    resideavaarea = fields.FloatField(default=0.00, null=True, blank=True)  # 可预（销）售住宅总面积
    limitarea = fields.FloatField(default=0.00, null=True, blank=True)  # 限制房产总面积
    dealnum = fields.IntField(default=0, null=True, blank=True)  # 已预（销）售总套数
    notnum = fields.IntField(default=0, null=True, blank=True)  # 未纳入网上销售房产套数
    dealarea = fields.FloatField(default=0.00, null=True, blank=True)  # 已预（销）售总面积
    notarea = fields.IntField(default=0, null=True, blank=True)  # 未纳入网上销售房产总面积
    plannum = fields.IntField(default=0, null=True, blank=True)  # 已预定套数
    planarea = fields.IntField(default=0, null=True, blank=True)  # 已预定总面积

    OpeningDate = fields.StringField(default='', max_length=100, null=True, blank=True)  # 开盘时间
    OpeningPrice = fields.FloatField(default=0.00, null=True, blank=True)  # 开盘价格
    ApprovalProjectName = fields.StringField(default='', max_length=100, null=True, blank=True)  # 预售审批项目名称
    PresellURL = fields.URLField(default=None, null=True, blank=True)  # 预售价地址
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
        ]
    }


class BuildingInfoWulumuqi(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingID = fields.StringField(default='', max_length=100, null=False)  # 楼栋id
    BuildingName = fields.StringField(default='', max_length=100, null=False)  # 楼栋名
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'BuildingUUID',
        ]
    }


class HouseInfoWulumuqi(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=100, null=False)  # 楼栋名
    UnitName = fields.StringField(default='', max_length=100, null=True, blank=True)  # 单元
    HouseNO = fields.StringField(default='', max_length=50)  # 户号
    RoughPrice = fields.StringField(default='', null=False)  # 毛坯单价
    HousePrice = fields.StringField(default='', null=False)  # 总价
    HouseBuildingArea = fields.StringField(default='', null=False)  # 建筑面积
    HouseInnerArea = fields.StringField(default='', null=False)  # 套内面积
    HouseState = fields.StringField(default='', max_length=50)  # 当前状态
    HouseStateLatest = fields.StringField(default='', max_length=255, null=False, blank=True)
    HouseType = fields.StringField(default='', max_length=50)  # 户型
    HouseFloor = fields.StringField(default='', null=False)  # 户楼层
    BuildingFloor = fields.StringField(default='', null=False)  # 总楼层
    HouseLocated = fields.StringField(default='', max_length=255)  # 坐落
    HouseUsage = fields.StringField(default='', max_length=50)  # 房屋用途
    HouseStructure = fields.StringField(default='', max_length=50)  # 房屋结构
    RoomRate = fields.StringField(default='', null=False)  # 得房率
    HouseManagementFees = fields.StringField(default='', null=False)  # 物业费
    HouseOrientation = fields.StringField(default='', max_length=50)  # 朝向
    DeclarationTime = fields.StringField(default='', max_length=50)  # 申报时间
    HouseURL = fields.URLField(default=None, null=True, blank=True)  # 户详情地址
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'BuildingUUID',
            'HouseUUID',
        ]
    }

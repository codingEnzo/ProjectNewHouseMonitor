# encoding = utf-8
import uuid
import datetime
from django_mongoengine import *
from django_mongoengine import fields


class ProjectInfoWuhan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    RealEstateProjectID = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)  # 项目名称
    HousingCount = fields.StringField(default='', max_length=255, null=False)  # 总套数(套)
    HouseSoldCount = fields.StringField(default='', max_length=255, null=False)  # 住房已售(套)
    HouseCount = fields.StringField(default='', max_length=255, null=False)  # 住房可售(套)
    UnHouseSoldCount = fields.StringField(default='', max_length=255, null=False)  # 非住房已售(套)
    UnHouseCount = fields.StringField(default='', max_length=255, null=False)  # 非住房可售(套)
    SourceUrl = fields.URLField(default=None, null=True, blank=True)

    ProjectAddress = fields.StringField(default='', max_length=255, null=False)  # 项目坐落
    EarliestStartDate = fields.StringField(default='', max_length=255, null=False)  # 开工时间
    CompletionDate = fields.StringField(default='', max_length=255, null=False)  # 竣工时间(预计)

    # 项目基本情况
    FloorArea = fields.StringField(default='', max_length=255, null=False)  # 用地面积
    PropertyRightsDescription = fields.StringField(default='', max_length=255, null=False)  # 土地使用年限
    LandUse = fields.StringField(default='', max_length=255, null=False)  # 土地用途
    LandLevel = fields.StringField(default='', max_length=255, null=False)  # 土地等级
    TotalBuidlingArea = fields.StringField(default='', max_length=255, null=False)  # 建筑面积
    FloorAreaRatio = fields.StringField(default='', max_length=255, null=False)  # 容积率
    HouseBuildingCount = fields.StringField(default='', max_length=255, null=False)  # 房屋栋数
    ProjectBookingData = fields.StringField(default='', max_length=255, null=False)  # 销售时间
    OtheRights = fields.StringField(default='', max_length=255, null=False)  # 他项权利情况

    # 项目证件情况
    LandUsePermit = fields.StringField(default='', max_length=255, null=False)  # 建设用地规划许可证号
    CertificateOfUseOfStateOwnedLand = fields.StringField(default='', max_length=255, null=False)  # 国有土地使用证号
    BuildingPermit = fields.StringField(default='', max_length=255, null=False)  # 建设工程规划许可证号
    ConstructionPermitNumber = fields.StringField(default='', max_length=255, null=False)  # 施工许可证号
    PresalePermitNumber = fields.StringField(default='', max_length=255, null=False)  # 商品房预售许可证号
    QualificationNumber = fields.StringField(default='', max_length=255, null=False)  # 开发企业资质证号
    Developer = fields.StringField(default='', max_length=255, null=False)  # 开发企业
    Contact = fields.StringField(default='', max_length=255, null=False)  # 联系电话
    PresaleRegistrationManagementDepartment = fields.StringField(default='', max_length=255, null=False)  # 项目备案机关

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'SourceUrl',
        ]
    }


class BuildingInfoWuhan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)  # 项目名称
    BuildingID = fields.StringField(default='', max_length=255, null=False)  # 楼栋ID
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)  # 楼栋名称
    BuildingStructure = fields.StringField(default='', max_length=255, null=False)  # 建筑结构
    Floors = fields.StringField(default='', max_length=255, null=False)  # 总层数
    HousingCount = fields.StringField(default='', max_length=255, null=False)  # 总套数
    SourceUrl = fields.URLField(default=None, null=True, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'BuildingUUID',
            'BuildingName',
            'SourceUrl',
        ]
    }


class HouseInfoWuhan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)

    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)  # 项目名称
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)  # 楼栋名称

    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=255, null=False)

    BuildingNumber = fields.StringField(default='', max_length=255, null=False)  # 栋号
    UnitName = fields.StringField(default='', max_length=255, null=False)  # 单元
    FloorName = fields.StringField(default='', max_length=255, null=False)  # 层名
    HouseState = fields.StringField(default='', max_length=50)  # 当前状态
    HouseStateLatest = fields.StringField(default='', max_length=255, null=False, blank=True)  # 上次状态
    HouseUrl = fields.URLField(default=None, null=True, blank=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'BuildingUUID',
            'BuildingName',
            'HouseUUID',
            'HouseName',
            'HouseState',
            'HouseStateLatest',
            'HouseUrl',
        ]
    }

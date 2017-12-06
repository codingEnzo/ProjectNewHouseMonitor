# encoding = utf-8
import uuid
import datetime
from django_mongoengine import *
from django_mongoengine import fields


# Guiyang City Model
class ProjectBaseGuiyang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(default='', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class ProjectInfoGuiyang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectUsage = fields.StringField(default='', max_length=1024, null=False)
    ProjectArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectDesignCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(default='', max_length=1024, null=False)
    ProjectSalePhone = fields.StringField(default='', max_length=1024, null=False)
    ProjectDescription = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectAreaCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectAreaPlanCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectEngPlanCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingCode = fields.StringField(default='', max_length=1024, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class BuildingInfoGuiyang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectRegName = fields.StringField(default=str(datetime.datetime.now()), index=True)
    BuildingCode = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoGuiyang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=1024, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseInfoText = fields.StringField(default='', max_length=1024, null=False)
    HouseUnit = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseNum = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(default='', max_length=1024, null=False)
    HouseType = fields.StringField(default='', max_length=1024, null=False)
    HouseReqURL = fields.StringField(default='', max_length=1024, null=False)
    HouseNumCheck = fields.StringField(default='', max_length=1024, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'BuildingName',
            'ProjectUUID',
            'BuildingUUID',
            'HouseUUID',
            'HouseName'
        ]
    }


# Taiyuan City Model
class ProjectBaseTaiyuan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(default='', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectType = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompanyId = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompanyName = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompanyCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompanyLevel = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompanyLevelCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompanyCorporation = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompanyCorporationPhone = fields.StringField(default='', max_length=1024, null=False)
    ProjectURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class ProjectInfoTaiyuan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleRange = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleBuildingNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleHouseNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectLHRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectRJRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildDate = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompleteDate = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectDesignCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectManageCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectUnitPrice = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompanmy = fields.StringField(default='', max_length=1024, null=False)
    ProjectUsage = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuilding = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegId = fields.StringField(default='', max_length=1024, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class BuildingInfoTaiyuan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    BuildingCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingMCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingBaseArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingShareArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingStructure = fields.StringField(default='', max_length=1024, null=False)
    BuildingYear = fields.StringField(default='', max_length=1024, null=False)
    BuildingFloorNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingFloorAbove = fields.StringField(default='', max_length=1024, null=False)
    BuildingFloorBelow = fields.StringField(default='', max_length=1024, null=False)
    BuildingUnitNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingSaleName = fields.StringField(default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoTaiyuan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=1024, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(default='', max_length=1024, null=False)
    HouseType = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleSubState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleSubStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseUnitPrice = fields.StringField(default='', max_length=1024, null=False)
    HouseAddress = fields.StringField(default='', max_length=1024, null=False)
    HouseId = fields.StringField(default='', max_length=1024, null=False)
    HouseCode = fields.StringField(default='', max_length=1024, null=False)
    HouseFloorTotal = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(default='', max_length=1024, null=False)
    HouseYear = fields.StringField(default='', max_length=1024, null=False)
    HouseGroundCode = fields.StringField(default='', max_length=1024, null=False)
    HouseGroundArea = fields.StringField(default='', max_length=1024, null=False)
    HouseGetGroundType = fields.StringField(default='', max_length=1024, null=False)
    HouseGroundType = fields.StringField(default='', max_length=1024, null=False)
    HouseGroundLimit = fields.StringField(default='', max_length=1024, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'BuildingName',
            'ProjectUUID',
            'BuildingUUID',
            'HouseUUID',
            'HouseName'
        ]
    }

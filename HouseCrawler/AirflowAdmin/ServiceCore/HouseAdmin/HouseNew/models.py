# encoding = utf-8
import datetime
import uuid

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


# 常州 ORM
class ProjectBaseChangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleNum = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleId = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleDate = fields.StringField(default='', max_length=255, null=False)
    ProjectURL = fields.StringField(default='', max_length=255, null=False)
    ProjectRecordURL = fields.StringField(default='', max_length=255, null=False)
    ProjectBuildingListURL = fields.StringField(default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectURL',
            'ProjectRecordURL',
            'ProjectBuildingListURL',
        ]
    }


class ProjectInfoChangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectRegion = fields.StringField(default='', max_length=255, null=False)
    # ProjectRegionNum = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleArea = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleHouseNum = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleBuildingRange = fields.StringField(default='', max_length=255, null=False)
    ProjectSalesAgency = fields.StringField(default='', max_length=255, null=False)
    ProjectSupervisorBank = fields.StringField(default='', max_length=255, null=False)
    ProjectSupervisorAccount = fields.StringField(default='', max_length=255, null=False)
    ProjectBankGuarantee = fields.StringField(default='', max_length=255, null=False)
    ProjectRecordsInfo = fields.ListField(default=[], max_length=1024, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectCompany',
        ]
    }


class BuildingInfoChangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleNum = fields.StringField(default='', max_length=255, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    BuildingURL = fields.StringField(default='', max_length=255, null=False)
    BuildingArea = fields.StringField(default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectPresaleNum',
            'BuildingUUID',
            'BuildingName'
        ]
    }


class HouseInfoChangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectPresaleNum = fields.StringField(default='', max_length=255, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=255, null=False)
    HouseContractPrice = fields.StringField(default='', max_length=255, null=False)
    HouseUsage = fields.StringField(default='', max_length=255, null=False)
    HouseLabel = fields.StringField(default='', max_length=255, null=False)
    HouseCurCell = fields.StringField(default='', max_length=255, null=False)
    HouseSaleStatus = fields.StringField(default='', max_length=255, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=255, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectPresaleNum',
            'BuildingUUID',
            'BuildingName',
            'HouseUUID',
            'HouseUsage',
            'HouseLabel',
            'HouseSaleStatus',
            'HouseSaleStateLatest'
        ]
    }


# Hefei City Model
class ProjectInfoHefei(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectID = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectManageCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectDevelopCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectMainStructure = fields.StringField(default='', max_length=1024, null=False)
    ProjectGreenRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectPlotRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectTranslateTimes = fields.StringField(default='', max_length=1024, null=False)
    ProjectTranslateRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(default='', max_length=1024, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectID',
            'ProjectName',
        ]
    }


class BuildingInfoHefei(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectID = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    BuildingStructure = fields.StringField(default='', max_length=1024, null=False)
    BuildingFloorAbove = fields.StringField(default='', max_length=1024, null=False)
    BuildingFloorBelow = fields.StringField(default='', max_length=1024, null=False)
    BuildingHouseNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingBusiness = fields.StringField(default='', max_length=1024, null=False)
    BuildingOfficeNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingOtherNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingAreaCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingPlanCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingUsage = fields.StringField(default='', max_length=1024, null=False)
    BuildingDesignCompany = fields.StringField(default='', max_length=1024, null=False)
    BuildingPreSellArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingOnlineSellArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingOpenDate = fields.StringField(default='', max_length=1024, null=False)
    BuildingCompleteDate = fields.StringField(default='', max_length=1024, null=False)
    BuildingDeliverDate = fields.StringField(default='', max_length=1024, null=False)
    BuildingAgent = fields.StringField(default='', max_length=1024, null=False)
    BuildingSellPhone = fields.StringField(default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectID',
            'ProjectUUID',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoHefei(Document):
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
    HouseID = fields.StringField(default='', max_length=1024, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(default='', max_length=1024, null=False)
    HouseType = fields.StringField(default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(default='', max_length=1024, null=False)
    HouseNum = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    HouseAddress = fields.StringField(default='', max_length=1024, null=False)
    HousePreSellPrice = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(default='', max_length=1024, null=False)

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


# Dalian Models
class ProjectBaseDalian(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(default='', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectURL',
        ]
    }


class ProjectInfoDalian(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(default='', max_length=1024, null=False)
    ProjectAreaPlanLicenseCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectPlanLicenseCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleSum = fields.DictField(default={'code': 0}, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class BuildingInfoDalian(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    BuildingRegName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingAddress = fields.StringField(default='', max_length=1024, null=False)
    BuildingHouseNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'BuildingRegName',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoDalian(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseInfoStr = fields.StringField(default='', max_length=1024, null=False)
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


class ProjectBaseDongguan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleSum = fields.StringField(default='', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectURL',
        ]
    }


class ProjectInfoDongguan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectUsage = fields.StringField(default='', max_length=1024, null=False)
    ProjectArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectHouseNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(default='', max_length=1024, null=False)
    ProjectAreaPlanLicenseCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectPlanLicenseCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectConstructionLicenseCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectConstructionCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectAuthenticFlag = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaledArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaledNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectUnavailableArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectUnavailableNum = fields.StringField(default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectRegName',
        ]
    }


class BuildingInfoDongguan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectRegName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingFloorNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingHouseNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingUsage = fields.StringField(default='', max_length=1024, null=False)
    BuildingSaleArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'ProjectRegName',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoDongguan(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseRecordState = fields.StringField(default='', max_length=1024, null=False)
    HouseRecordStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HousePledgeState = fields.StringField(default='', max_length=1024, null=False)
    HousePledgeStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseAttachState = fields.StringField(default='', max_length=1024, null=False)
    HouseAttachStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='0.0', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(default='0.0', max_length=1024, null=False)
    HouseShareArea = fields.StringField(default='0.0', max_length=1024, null=False)
    HouseUnitPrice = fields.StringField(default='0.0', null=False)
    HousePrice = fields.StringField(default='0.0', null=False)
    HousePriceFlag = fields.BooleanField(default=False, null=False)
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


class ProjectBaseChangsha(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                      binary=False, null=False)
    ProjectRegName = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegDate = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class ProjectInfoChangsha(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(default='', max_length=1024, null=False)
    ProjectBaseLicenseCode = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectBasePrice = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectSalePhone = fields.StringField(default='', max_length=1024, null=False)
    ProjectHouseNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectBusLine = fields.StringField(default='', max_length=1024, null=False)
    ProjectTotalArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectDesignCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleAgent = fields.StringField(default='', max_length=1024, null=False)
    ProjectManageCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectFinishAt = fields.StringField(default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class BuildingInfoChangsha(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegName = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegDate = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingAreaLicenceCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingEngPlanLicenceCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingAreaPlanLicenceCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingBuildLicenceCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegArea = fields.StringField(default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'BuildingRegName',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoChangsha(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(default='', max_length=1024, null=False)
    HouseType = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseDType = fields.StringField(default='', max_length=1024, null=False)
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


class ProjectBaseHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)

    PropertyID = fields.StringField(default='', max_length=100, null=False)  # 楼盘id
    sid = fields.StringField(default='33', max_length=100, null=False)  # sid

    ProjectAllrankvalue = fields.StringField(default='', max_length=100)  # 综合评分
    ProjectName = fields.StringField(default='', max_length=200, null=False)  # 楼盘名称
    PromotionName = fields.StringField(default='', max_length=100)  # 推广名
    DistrictName = fields.StringField(default='', max_length=100)  # 行政区
    RegionName = fields.StringField(default='', max_length=100)  # 街道
    ProjectAddress = fields.StringField(default='', null=False)  # 楼盘地址
    ProjectSellAddress = fields.StringField(default='')  # 售楼地址
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


class PresellInfoHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)  # 创建时间
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellID = fields.StringField(default='', max_length=100, null=False)  # 预售证id
    PropertyID = fields.StringField(default='', max_length=100, null=False)  # 预售证id
    sid = fields.StringField(default='', max_length=100, index=True, null=False)  # sid
    PresellNO = fields.StringField(default='')  # 预售证号/预售证编号
    PresellName = fields.StringField(default='')  # 预售证号/预售证编号

    LssueDate = fields.StringField(default='', max_length=100)  # 预售证核发时间
    Applycorp = fields.StringField(default='', max_length=100)  # 预售证申领单位
    LssuingAuthority = fields.StringField(default='', max_length=100)  # 发证机关

    Bank = fields.StringField(default='', max_length=100)  # 资金监管银行
    BankAccount = fields.StringField(default='', max_length=100)  # 资金监管银行账号
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

    OpeningDate = fields.StringField(default='', max_length=100)  # 开盘时间
    ApprovalProjectName = fields.StringField(default='', max_length=100)  # 预售审批项目名称
    PresellURL = fields.URLField(default=None, null=True, blank=True)  # 预售价地址
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
        ]
    }


class BuildingInfoHangzhou(Document):
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


class HouseInfoHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=100, null=False)  # 楼栋名
    UnitName = fields.StringField(default='', max_length=100, null=True, blank=True)  # 单元
    HouseNO = fields.StringField(default='', max_length=255)  # 户号
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
            'HouseState',
            'HouseStateLatest',
        ]
    }


class IndexHouseInfoHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    RegionUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    Region = fields.StringField(default='', null=False)
    SignCount = fields.StringField(default='', null=False)
    BookCount = fields.StringField(default='', null=False)
    SaleCount = fields.StringField(default='', null=False)


class IndexInfoHangzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    RegionUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    Region = fields.StringField(default='', null=False)
    SignCount = fields.StringField(default='', null=False)
    SaleArea = fields.StringField(default='', null=False)


# Chongqing Model
class ProjectBaseChongqing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectBaseName = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(default='', max_length=1024, null=False)
    ProjectSoldNum = fields.StringField(default='0', max_length=1024, null=False)
    ProjectSoldArea = fields.StringField(default='0.0', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectCorporation'
        ]
    }


class BuildingInfoChongqing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectBaseName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingZZHouseNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingFZZHouseNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingZZHouseNumSaling = fields.StringField(default='', max_length=1024, null=False)
    BuildingFZZHouseNumSaling = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegHouseNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectBaseName',
            'ProjectName',
            'ProjectUUID',
            'BuildingRegName',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoChongqing(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                 binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=1024, null=False)
    HoueseID = fields.StringField(default='', max_length=1024, null=False)
    HoueseRegID = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseRoomNum = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(default='', max_length=1024, null=False)
    HouseRoomType = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateCode = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseInnerUnitPrice = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingUnitPrice = fields.StringField(default='', max_length=1024, null=False)
    HouseType = fields.StringField(default='', max_length=1024, null=False)
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


# Nanchang Model
class ProjectBaseNanchang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectHouseSalingNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectOtherSalingNum = fields.StringField(default='', max_length=1024, null=False)
    ProjectSalingArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class ProjectInfoNanchang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(default='', max_length=1024, null=False)
    ProjectSalePhone = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectUsage = fields.StringField(default='', max_length=1024, null=False)
    ProjectArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectUseArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectRongjiRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectLvdiRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectInvestment = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildDate = fields.StringField(default='', max_length=1024, null=False)
    ProjectCompleteDate = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectMeasureCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectSaleSum = fields.DictField(default={'null': ''}, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class BuildingInfoNanchang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUsage = fields.StringField(default='', max_length=1024, null=False)
    BuildingStructure = fields.StringField(default='', max_length=1024, null=False)
    BuildingTotalFloor = fields.StringField(default='', max_length=1024, null=False)
    BuildingTotalArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingSaleSum = fields.DictField(default={'null': ''}, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoNanchang(Document):
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
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseFloorAt = fields.StringField(default='', max_length=1024, null=False)
    HouseFloorTotal = fields.StringField(default='', max_length=1024, null=False)
    HousePreUnitPrice = fields.StringField(default='', max_length=1024, null=False)
    HouseStructureType = fields.StringField(default='', max_length=1024, null=False)
    HouseContract = fields.StringField(default='', max_length=1024, null=False)
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


class ProjectBaseNantong(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    ReferencePrice = fields.StringField(default='', max_length=255)  # 参考价格
    OnSaleState = fields.StringField(default='', max_length=100, null=False)  # 楼盘状态/在售状态
    LandUse = fields.StringField(default='', max_length=255)  # 土地用途
    Developer = fields.StringField(default='', max_length=255)  # 开发商
    Selltel = fields.StringField(default='', max_length=100)  # 销售热线
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 项目链接


class ProjectInfoNantong(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    OnSaleState = fields.StringField(default='', max_length=100, null=False)  # 楼盘状态/在售状态
    LandUse = fields.StringField(default='', max_length=255)  # 土地用途
    RecordName = fields.StringField(default='', max_length=255)  # 备案名
    Decoration = fields.StringField(default='', max_length=255)  # 装修
    HousingCount = fields.StringField(default='', max_length=255)  # 规划户数
    Developer = fields.StringField(default='', max_length=255)  # 开发商
    DistrictName = fields.StringField(default='', max_length=255)  # 行政区
    ProjectAddress = fields.StringField(default='', max_length=255)  # 项目地址
    ApprovalPresaleAmount = fields.StringField(default='', max_length=255)  # 批准预售总套数
    HousingOnsoldAmount = fields.StringField(default='', max_length=255)  # 住宅可售套数
    ReferencePrice = fields.StringField(default='', max_length=255)  # 参考价格
    EarliestOpeningTime = fields.StringField(default='', max_length=255)  # 开盘时间
    LatestDeliversHouseDate = fields.StringField(default='', max_length=255)  # 交房时间
    FloorArea = fields.StringField(default='', max_length=100)  # 占地面积
    TotalBuidlingArea = fields.StringField(default='', max_length=100)  # 建筑面积
    FloorAreaRatio = fields.StringField(default='', max_length=100)  # 容积率
    GreeningRate = fields.StringField(default='', max_length=100)  # 绿化率
    ManagementFees = fields.StringField(default='', max_length=100)  # 物业费
    ManagementCompany = fields.StringField(default='', max_length=100)  # 物业公司
    BuildingType = fields.StringField(default='', max_length=100)  # 建筑类别
    ProjectSellAddress = fields.StringField(default='')  # 售楼地址
    SalesAgent = fields.StringField(default='')  # 销售代理
    ConstructionUnit = fields.StringField(default='')  # 施工单位
    ProjectIntro = fields.StringField(default='')  # 项目简介
    ProjectAroundSupporting = fields.StringField(default='')  # 周边配套
    TrafficSituation = fields.StringField(default='')  # 交通情况
    DecorationInfo = fields.StringField(default='')  # 装修情况
    DeveloperIntro = fields.StringField(default='')  # 开发商介绍
    AboutInfo = fields.StringField(default='')  # 相关信息
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 项目详细URL
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'OnSaleState',
            'ApprovalPresaleAmount',
            'HousingOnsoldAmount',
            'ReferencePrice',
            'SourceUrl',
        ]
    }


class PresellInfoNantong(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    PresellUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    PresalePermitNumber = fields.StringField(default='', max_length=255)  # 预售证编号
    ApprovalPresaleArea = fields.StringField(default='', max_length=255)  # 批准预售面积
    ApprovalPresaleBuildingName = fields.StringField(default='')  # 批准销售房层幢号
    Price = fields.StringField(default='')  # 房层价格
    LssueDate = fields.StringField(default='', max_length=255)  # 批准日期
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'PresellUUID',
            'ProjectName',
            'PresalePermitNumber',
        ]
    }


class BuildingInfoNantong(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    PresalePermitNumber = fields.StringField(default='', max_length=255)  # 预售证编号
    BuildingName = fields.StringField(default='', max_length=255)  # 楼栋名
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 楼栋销控表链接
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'BuildingUUID',
            'SourceUrl',
        ]
    }


class HouseInfoNantong(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()))
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''), binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255)  # 项目名称
    BuildingName = fields.StringField(default='', max_length=255)  # 楼栋名称
    FloorName = fields.StringField(default='', max_length=255)  # 层名
    HouseNumber = fields.StringField(default='', max_length=255)  # 房号
    HouseState = fields.StringField(default='', max_length=255)  # 当前状态
    HouseStateLatest = fields.StringField(default='', max_length=255)  # 上次状态
    MeasuredBuildingArea = fields.StringField(default='', max_length=255)  # 建筑面积
    MeasuredInsideOfBuildingArea = fields.StringField(default='', max_length=255)  # 套内面积
    MeasuredSharedPublicArea = fields.StringField(default='', max_length=255)  # 公摊面积
    HouseUseType = fields.StringField(default='', max_length=255)  # 房屋功能/用途
    UnitShape = fields.StringField(default='', max_length=255)  # 户型
    TotalPrice = fields.StringField(default='', max_length=255)  # 总价
    SourceUrl = fields.URLField(default=None, null=True, blank=True)  # 户详细URL
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'BuildingUUID',
            'HouseUUID',
            'HouseState',
            'HouseStateLatest',
            'SourceUrl',
        ]
    }


class ProjectBaseQuanzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectURL = fields.StringField(default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class ProjectInfoQuanzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(default='', max_length=1024, null=False)
    ProjectPhone = fields.StringField(default='', max_length=1024, null=False)
    ProjectPhoneConn = fields.StringField(default='', max_length=1024, null=False)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class BuildingInfoQuanzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingRegName = fields.StringField(default='', max_length=1024, null=False)
    BuildingArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingDistrict = fields.StringField(default='', max_length=1024, null=False)
    BuildingAddress = fields.StringField(default='', max_length=1024, null=False)
    BuildingBuildDate = fields.StringField(default='', max_length=1024, null=False)
    BuildingCompleteDate = fields.StringField(default='', max_length=1024, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)

    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoQuanzhou(Document):
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
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseNum = fields.StringField(default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)

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


class ProjectBaseJiujiang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectDescription = fields.DynamicField(default='', null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class ProjectInfoJiujiang(Document):
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
    ProjectRongjiRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectLvdiRatio = fields.StringField(default='', max_length=1024, null=False)
    ProjectInvestment = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildDate = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildingCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectManageCompany = fields.StringField(default='', max_length=1024, null=False)
    ProjectDesignCompany = fields.StringField(default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
        ]
    }


class BuildingInfoJiujiang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingRegName = fields.StringField(default='', max_length=1024, null=False)
    BuildingArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegDate = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegPrice = fields.StringField(default='', max_length=1024, null=False)
    BuildingSalingNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingType = fields.StringField(default='', max_length=1024, null=False)
    BuildingSaleState = fields.StringField(default='', max_length=1024, null=False)
    BuildingSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    BuildingPlanAreaCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingPlanEngCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingBuildEngCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingAreaCode = fields.StringField(default='', max_length=1024, null=False)
    BuildingZZHouseNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingFZZHouseNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingSoldNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingZZUnitPrice = fields.StringField(default='', max_length=1024, null=False)
    BuildingFZZUnitPrice = fields.StringField(default='', max_length=1024, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfoJiujiang(Document):
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
    HouseOSEQ = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseKey = fields.StringField(default='', max_length=1024, null=False)
    HouseSTR_2 = fields.StringField(default='', max_length=1024, null=False)
    HouseSTR_3 = fields.StringField(default='', max_length=1024, null=False)
    HouseSTR_5 = fields.StringField(default='', max_length=1024, null=False)
    HouseSattribute = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseUnitPrice = fields.StringField(default='', max_length=1024, null=False)
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


# class ProjectCountInfoJiujiang(Document):
#     RecordID = fields.UUIDField(default=uuid.uuid1(),
#                                     binary=True, primary_key=True, null=False)
#     CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
#     ProjectSalingNum = fields.IntField(default=0, index=True)
#     ProjectSaledNum = fields.IntField(default=0, index=True)
#     meta = {
#         'indexes': [
#             'RecordID',
#             'CurTimeStamp',
#         ]
#     }
#
#
# class BuildingCountInfoJiujiang(Document):
#     RecordID = fields.UUIDField(default=uuid.uuid1(),
#                                     binary=True, primary_key=True, null=False)
#     CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
#     BuildingSalingNum = fields.IntField(default=0, index=True)
#     BuildingSaledNum = fields.IntField(default=0, index=True)
#     meta = {
#         'indexes': [
#             'RecordID',
#             'CurTimeStamp',
#         ]
#     }
#
#
# class HouseCountInfoJiujiang(Document):
#     RecordID = fields.UUIDField(default=uuid.uuid1(),
#                                     binary=True, primary_key=True, null=False)
#     CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
#     HouseUnavailableNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
#     HouseAvailableNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
#     HouseReserveNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
#     HouseContractNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
#     HouseRecordNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
#     HouseAuditNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
#     meta = {
#         'indexes': [
#             'RecordID',
#             'CurTimeStamp',
#         ]
#     }

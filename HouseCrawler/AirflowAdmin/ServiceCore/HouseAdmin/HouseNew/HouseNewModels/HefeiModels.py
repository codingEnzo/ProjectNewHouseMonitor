# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


# Hefei City Model
class ProjectInfoHefei(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectID = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectManageCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectDevelopCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildingArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectMainStructure = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectGreenRatio = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectPlotRatio = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectTranslateTimes = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectTranslateRatio = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(
        default='', max_length=1024, null=False)

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
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectID = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegName = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    BuildingStructure = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingFloorAbove = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingFloorBelow = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingHouseNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingBusiness = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingOfficeNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingOtherNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingAreaCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingPlanCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingUsage = fields.StringField(default='', max_length=1024, null=False)
    BuildingDesignCompany = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingPreSellArea = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingOnlineSellArea = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingOpenDate = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingCompleteDate = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingDeliverDate = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingAgent = fields.StringField(default='', max_length=1024, null=False)
    BuildingSellPhone = fields.StringField(
        default='', max_length=1024, null=False)
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
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
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
    HouseFloor = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(
        default='', max_length=1024, null=False)
    HouseType = fields.StringField(default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseNum = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseAddress = fields.StringField(default='', max_length=1024, null=False)
    HousePreSellPrice = fields.StringField(
        default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(
        default='', max_length=1024, null=False)

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

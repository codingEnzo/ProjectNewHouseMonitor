# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


# Nanchang Model
class ProjectBaseNanchang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectHouseSalingNum = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectOtherSalingNum = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSalingArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectURLCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
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
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSalePhone = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectUsage = fields.StringField(default='', max_length=1024, null=False)
    ProjectArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectUseArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectRongjiRatio = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectLvdiRatio = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildingRatio = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectInvestment = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildDate = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectCompleteDate = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildingCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectMeasureCompany = fields.StringField(
        default='', max_length=1024, null=False)
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
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUsage = fields.StringField(default='', max_length=1024, null=False)
    BuildingStructure = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingTotalFloor = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingTotalArea = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingSaleSum = fields.DictField(default={'null': ''}, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
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
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
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
    HouseSaleState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(
        default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseFloorAt = fields.StringField(default='', max_length=1024, null=False)
    HouseFloorTotal = fields.StringField(
        default='', max_length=1024, null=False)
    HousePreUnitPrice = fields.StringField(
        default='', max_length=1024, null=False)
    HouseStructureType = fields.StringField(
        default='', max_length=1024, null=False)
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

# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseJiujiang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectDescription = fields.DynamicField(default='', null=False)
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


class ProjectInfoJiujiang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectUsage = fields.StringField(default='', max_length=1024, null=False)
    ProjectArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectBuildArea = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectRongjiRatio = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectLvdiRatio = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectInvestment = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildDate = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildingCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectManageCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectDesignCompany = fields.StringField(
        default='', max_length=1024, null=False)
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
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingRegName = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegDate = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingRegPrice = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingSalingNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingType = fields.StringField(default='', max_length=1024, null=False)
    BuildingSaleState = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingSaleStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingPlanAreaCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingPlanEngCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingBuildEngCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingAreaCode = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingZZHouseNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingFZZHouseNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingSoldNum = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingZZUnitPrice = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingFZZUnitPrice = fields.StringField(
        default='', max_length=1024, null=False)
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


class HouseInfoJiujiang(Document):
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
    HouseOSEQ = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseKey = fields.StringField(default='', max_length=1024, null=False)
    HouseSTR_2 = fields.StringField(default='', max_length=1024, null=False)
    HouseSTR_3 = fields.StringField(default='', max_length=1024, null=False)
    HouseSTR_5 = fields.StringField(default='', max_length=1024, null=False)
    HouseSattribute = fields.StringField(
        default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HouseUnitPrice = fields.StringField(
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

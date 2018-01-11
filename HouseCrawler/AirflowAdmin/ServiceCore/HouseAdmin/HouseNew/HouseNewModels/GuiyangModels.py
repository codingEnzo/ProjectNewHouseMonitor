# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields

# Guiyang City Model


class ProjectBaseGuiyang(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(
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


class ProjectInfoGuiyang(Document):
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
    ProjectBuildingCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectDesignCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectRegName = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectSalePhone = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectDescription = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildingNum = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAreaCode = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAreaPlanCode = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectEngPlanCode = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectBuildingCode = fields.StringField(
        default='', max_length=1024, null=False)

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
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectRegName = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    BuildingCode = fields.StringField(
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


class HouseInfoGuiyang(Document):
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
    HouseInfoText = fields.StringField(default='', max_length=1024, null=False)
    HouseUnit = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseNum = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(
        default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(
        default='', max_length=1024, null=False)
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

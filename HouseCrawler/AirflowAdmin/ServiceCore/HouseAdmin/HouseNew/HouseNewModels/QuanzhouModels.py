# encoding = utf-8
import datetime
import uuid

from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseQuanzhou(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
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
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                   binary=False, null=False)
    ProjectCompany = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectArea = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(
        default='', max_length=1024, null=False)
    ProjectPhone = fields.StringField(default='', max_length=1024, null=False)
    ProjectPhoneConn = fields.StringField(
        default='', max_length=1024, null=False)

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
    BuildingNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingDistrict = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingAddress = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingBuildDate = fields.StringField(
        default='', max_length=1024, null=False)
    BuildingCompleteDate = fields.StringField(
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


class HouseInfoQuanzhou(Document):
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
    HouseNum = fields.StringField(default='', max_length=1024, null=False)
    HouseStructure = fields.StringField(
        default='', max_length=1024, null=False)
    HouseUsage = fields.StringField(default='', max_length=1024, null=False)
    HouseBuildingArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseInnerArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseShareArea = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleState = fields.StringField(
        default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(
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

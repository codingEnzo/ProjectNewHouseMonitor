# encoding = utf-8
import uuid
import datetime
from django_mongoengine import *
from django_mongoengine import fields


class ProjectBase(Document):
    TYPE = ((0, '期房'),
            (1, '现房'))
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectType = fields.IntField(default=0, choices=TYPE, null=False)
    ProjectURL = fields.URLField(default=None, null=True, blank=True)
    ProjectRegName = fields.StringField(default='', max_length=255, null=False)
    ProjectRegTime = fields.StringField(default='', max_length=255, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectType',
            'ProjectURL',
            'ProjectRegName',
            'ProjectRegTime'
        ]
    }


class ProjectInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    SubProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                        binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectAddress = fields.StringField(default='', max_length=255, null=False)
    SubProjectAddress = fields.StringField(default='', max_length=255, null=False)
    ProjectCompany = fields.StringField(default='', max_length=255, null=False)
    ProjectCorporation = fields.StringField(default='', max_length=255, null=False)
    ProjectCorporationCode = fields.StringField(default='', max_length=255, null=False)
    ProjectRegName = fields.StringField(default='', max_length=255, null=False)
    ProjectRegTime = fields.StringField(default='', max_length=255, null=False)
    ProjectLicenseCode = fields.StringField(default='', max_length=255, null=False)
    ProjectLicenseDate = fields.StringField(default='', max_length=255, null=False)
    ProjectUsage = fields.StringField(default='', max_length=255, null=False)
    ProjectArea = fields.StringField(default='', max_length=255, null=False)
    ProjectSaleSum = fields.DictField(default={'null': True}, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'SubProjectUUID',
            'ProjectName',
            'ProjectRegName',
            'ProjectRegTime',
            'ProjectLicenseCode',
            'ProjectLicenseDate',
        ]
    }


class BuildingInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    SubProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                        binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    BuildingSaleNum = fields.IntField(default=0, null=False)
    BuildingSaleArea = fields.FloatField(default=0.0, null=False)
    BuildingSaleStatus = fields.StringField(default='', max_length=255, null=False)
    BuildingSaleStatusLatest = fields.StringField(default='', max_length=255, null=False)
    BuildingSalePrice = fields.FloatField(default=0.0, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'BuildingUUID',
            'BuildingName',
            'BuildingSaleStatus',
            'BuildingSaleStatusLatest',
        ]
    }


class HouseInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    SubProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                        binary=False, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    HouseName = fields.StringField(default='', max_length=255, null=False)
    HouseFloor = fields.StringField(default='', max_length=255, null=False)
    HouseFloorSale = fields.StringField(default='', max_length=255, null=False)
    HouseState = fields.StringField(default='', max_length=255, null=False)
    HouseStateLatest = fields.StringField(default='', max_length=255, null=False)
    HouseSubState = fields.StringField(default='', max_length=255, null=False)
    HouseSubStateLatest = fields.StringField(default='', max_length=255, null=False)
    HouseUsage = fields.StringField(default='', max_length=255, null=False)
    HouseStructure = fields.StringField(default='', max_length=255, null=False)
    HouseBuildingArea = fields.FloatField(default=0.0, null=False)
    HouseInnerArea = fields.FloatField(default=0.0, null=False)
    HouseBuildingUnitPrice = fields.FloatField(default=0.0, null=False)
    HouseInnerUnitPrice = fields.FloatField(default=0.0, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'BuildingName',
            'HouseUUID',
            'HouseName',
            'HouseFloor',
            'HouseFloorSale',
            'HouseState',
            'HouseStateLatest',
            'HouseSubState',
            'HouseSubStateLatest',
        ]
    }

# encoding = utf-8
import uuid
import datetime
from django_mongoengine import *
from django_mongoengine import fields


class ProjectBase(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectDistrict = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(default='', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectCorporation'
        ]
    }


class ProjectInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(default='', max_length=1024, null=False)
    ProjectSoldNum = fields.StringField(default='0', max_length=1024, null=False)
    ProjectArea = fields.StringField(default='0.0', max_length=1024, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'ProjectCorporation'
        ]
    }


class BuildingInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    ProjectName = fields.StringField(default='', max_length=1024, null=False)
    SubProjectUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    SubProjectName = fields.StringField(default='', max_length=1024, null=False)
    ProjectAddress = fields.StringField(default='', max_length=1024, null=False)
    ProjectCorporation = fields.StringField(default='', max_length=1024, null=False)
    BuildingRegName = fields.StringField(default='', max_length=1024, null=False)
    BuildingUUID = fields.UUIDField(default=uuid.uuid3(uuid.NAMESPACE_DNS, ''),
                                    binary=False, null=False)
    BuildingName = fields.StringField(default='', max_length=1024, null=False)
    BuildingHouseNum = fields.StringField(default='', max_length=1024, null=False)
    BuildingArea = fields.StringField(default='', max_length=1024, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    BuildingURLCurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectName',
            'ProjectUUID',
            'SubProjectUUID',
            'SubProjectName',
            'BuildingRegName',
            'BuildingUUID',
            'BuildingName',
        ]
    }


class HouseInfo(Document):
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
    HouseSaleState = fields.StringField(default='', max_length=1024, null=False)
    HouseSaleStateLatest = fields.StringField(default='', max_length=1024, null=False)
    HouseInfoStr = fields.StringField(default='', max_length=1024, null=False)


    HoueseID = fields.StringField(default='', max_length=1024, null=False)
    HoueseRegID = fields.StringField(default='', max_length=1024, null=False)
    HouseFloor = fields.StringField(default='', max_length=1024, null=False)
    HouseRoomNum = fields.StringField(default='', max_length=1024, null=False)
    "y":13,
    "x":2,
    "bArea":116.3,
    "iArea":85.74,
    "vArea":0,
    "sArea":30.56,
    "shareRate":0,
    "uArea":0,
    "prebArea":0,
    "preiArea":0,
    "prevArea":0,
    "presArea":0,
    "preShareRate":0,
    "preuArea":0,
    "stru":"钢筋混凝土结构",
    "struId":0,
    "rType":"二室二厅",
    "rTypeId":0,
    "landOwnType":0,
    "landKind":0,
    "landParcelMemoId":0,
    "useId":0,
    "landUserId":0,
    "use":"成套住宅",
    "noSale":false,
    "memo":null,
    "u":0,
    "d":0,
    "l":0,
    "r":0,
    "status":2621452,
    "stasn":null,
    "stan":null,
    "pid":0,
    "ex1":null,
    "tag":"11064585",
    "unitnumber":"1",
    "block":"1",
    "roomIid":null,
    "location":"渝中区嘉滨路3号3-2",
    "siteId":0,
    "storeyHeight":0,
    "floorUse":0,
    "verandas":0,
    "areaType":0,
    "preSalearea":0,
    "saleArea":0,
    "parcelUsearea":0,
    "parecelSharearea":0,
    "state":0,
    "publicField":null,
    "parcelStartDate":null,
    "parcelEndDate":null,
    "isUnion":0,
    "nsjg":45600,
    "nsjmjg":33600,
    "sellerId":0,
    "enterpriseId":0,
    "district":0,
    "rightKindId":0,
    "rightTypeId":0,
    "f_zxsp_name":null,
    "zxsp":0,
    "yslx":null,
    "isYjs":0,
    "ysxgsj":null,
    "beizu":null,
    "fsbw":null,
    "F_ISONLINESIGN":1,
    "F_ISCONTRACT":1,
    "F_ISOTHERRIGHT":0,
    "F_ISOWNERSHIP":0,
    "F_ISLIMIT":0,
    "F_ISUSE":0,
    "S_ISONLINESIGN":null,
    "S_ISCONTRACT":null,
    "S_ISOTHERRIGHT":null,
    "S_ISOWNERSHIP":null,
    "S_ISLIMIT":null,
    "S_ISUSE":null,
    "F_PRESALE_CERT":null,
    "F_HOUSE_NO":"YZ00600600790000010100100130002",
    "F_FJH":null,
    "F_STATE":"期房",
    "F_Business_Status":null,
    "f_nosale_memo":"",
    "F_Total":0



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


class ProjectCountInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    ProjectSalingNum = fields.IntField(default=0, index=True)
    ProjectSaledNum = fields.IntField(default=0, index=True)
    meta = {
        'indexes': [
            'RecordID',
            'CurTimeStamp',
        ]
    }


class BuildingCountInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    BuildingSalingNum = fields.IntField(default=0, index=True)
    BuildingSaledNum = fields.IntField(default=0, index=True)
    meta = {
        'indexes': [
            'RecordID',
            'CurTimeStamp',
        ]
    }


class HouseCountInfo(Document):
    RecordID = fields.UUIDField(default=uuid.uuid1(),
                                    binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(datetime.datetime.now()), index=True)
    HouseUnavailableNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseAvailableNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseReserveNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseContractNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseRecordNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    HouseAuditNum = fields.DictField(default={'dafault': 0, 'pledged': 0}, index=True)
    meta = {
        'indexes': [
            'RecordID',
            'CurTimeStamp',
        ]
    }

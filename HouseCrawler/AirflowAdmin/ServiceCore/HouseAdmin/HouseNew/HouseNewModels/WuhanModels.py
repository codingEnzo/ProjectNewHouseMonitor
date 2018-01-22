# encoding = utf-8
import uuid
import datetime
from django_mongoengine import *
from django_mongoengine import fields


class ProjectBaseWuhan(Document):
    TYPE = ((0, '已售房'),
            (1, '可售房')),
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(default=str(
        datetime.datetime.now()), max_length=255, index=True)
    ProjectUUID = fields.StringField(default='', max_length=255, null=False)
    ProjectUrl = fields.URLField(default=None, null=True, blank=True)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    Allnumber = fields.StringField(default='', max_length=255, null=False)
    Home_have_sale = fields.StringField(default='', max_length=255, null=False)
    Home_sale = fields.StringField(default='', max_length=255, null=False)
    NoHome_have_sale = fields.StringField(
        default='', max_length=255, null=False)
    NoHome_sale = fields.StringField(default='', max_length=255, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'Allnumber',
            'Home_have_sale',
            'Home_sale',
            'NoHome_have_sale',
            'NoHome_sale',
        ]
    }


class ProjectInfoWuhan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.StringField(default='', max_length=255, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    InfoUrl = fields.URLField(default=None, null=True, blank=True)
    location = fields.StringField(default='', max_length=255, null=False)
    start_work_time = fields.StringField(
        default='', max_length=255, null=False)
    completed_time = fields.StringField(default='', max_length=255, null=False)
    land_area = fields.StringField(default='', max_length=255, null=False)
    building_area = fields.StringField(default='', max_length=255, null=False)
    land_year = fields.StringField(default='', max_length=255, null=False)
    land_purpose = fields.StringField(default='', max_length=255, null=False)
    home_Tnumber = fields.StringField(default='', max_length=255, null=False)
    home_Dnumber = fields.StringField(default='', max_length=255, null=False)
    market_time = fields.StringField(default='', max_length=255, null=False)
    His_rights = fields.StringField(default='', max_length=255, null=False)
    Phone1 = fields.StringField(default='', max_length=255, null=False)
    Phone2 = fields.StringField(default='', max_length=255, null=False)
    AgencyCompany = fields.StringField(default='', max_length=255, null=False)
    Volume_rate = fields.StringField(default='', max_length=255, null=False)
    Land_grade = fields.StringField(default='', max_length=255, null=False)
    PermitNumberOfConstructionLandPlanning = fields.StringField(
        default='', max_length=255, null=False)
    CertificateOfUseOfStateOwnedLand = fields.StringField(
        default='', max_length=255, null=False)
    ConstructionProjectPlanningPermitNumber = fields.StringField(
        default='', max_length=255, null=False)
    ConstructionPermitNumber = fields.StringField(
        default='', max_length=255, null=False)
    LicenseNumberOfCommercialHousingPresale = fields.StringField(
        default='', max_length=820, null=False)
    DevelopEnterpriseQualificationNumber = fields.StringField(
        default='', max_length=255, null=False)
    DevelopmentEnterprise = fields.StringField(
        default='', max_length=255, null=False)
    ProjectFilingAuthority = fields.StringField(
        default='', max_length=255, null=False)
    meta = {
        'indexes': [
            'CurTimeStamp',
            'ProjectUUID',
            'ProjectName',
            'location',
            'start_work_time',
            'completed_time',
            'land_area',
            'building_area',
            'land_year',
            'land_purpose',
            'home_Tnumber',
            'home_Dnumber',
            'market_time',
            'His_rights',
            'Phone1',
            'AgencyCompany',
            'Phone2',
            'Volume_rate',
            'Land_grade',
            'PermitNumberOfConstructionLandPlanning',
            'CertificateOfUseOfStateOwnedLand',
            'ConstructionProjectPlanningPermitNumber',
            'ConstructionPermitNumber',
            'LicenseNumberOfCommercialHousingPresale',
            'DevelopEnterpriseQualificationNumber',
            'DevelopmentEnterprise',
            'ProjectFilingAuthority',
        ]
    }


class BuildingInfoWuhan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    ProjectUUID = fields.StringField(default='', max_length=255, null=False)
    BuildingUUID = fields.StringField(default='', max_length=255, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    Building_structure = fields.StringField(
        default='', max_length=255, null=False)
    Layer_number = fields.StringField(default='', max_length=255, null=False)
    Set_number = fields.StringField(default='', max_length=255, null=False)
    BuildingURL = fields.URLField(default=None, null=True, blank=True)
    meta = {
        'indexes': [
            'BuildingUUID',
            'ProjectUUID',
            'CurTimeStamp',
            'BuildingName',
            'BuildingURL',
            'Building_structure',
            'Layer_number',
            'Set_number',
        ]
    }


class HouseInfoWuhan(Document):

    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    HouseUUID = fields.StringField(default='', max_length=255, null=False)
    ProjectUUID = fields.StringField(default='', max_length=255, null=False)
    BuildingUUID = fields.StringField(default='', max_length=255, null=False)
    ProjectName = fields.StringField(default='', max_length=255, null=False)
    BuildingName = fields.StringField(default='', max_length=255, null=False)
    HouseName = fields.StringField(default='', max_length=255, null=False)
    BuildingNum = fields.StringField(default='', max_length=255, null=False)
    Unit = fields.StringField(default='', max_length=255, null=False)
    FloorNum = fields.StringField(default='', max_length=255, null=False)
    HouseUrl = fields.URLField(default=None, null=True, blank=True)
    HouseSubUrl = fields.StringField(default='', max_length=255, null=False)
    State = fields.StringField(default='', max_length=255, null=False)
    House_located = fields.StringField(default='', max_length=255, null=False)
    Pre_sale_license_number = fields.StringField(
        default='', max_length=255, null=False)
    Predicted_area = fields.StringField(default='', max_length=255, null=False)
    Measured_area = fields.StringField(default='', max_length=255, null=False)
    Record_unit_price = fields.StringField(
        default='', max_length=255, null=False)
    StateLatest = fields.StringField(default='', max_length=1023, null=False)
    NewCurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    meta = {
        'indexes': [
            'HouseUUID',
            'BuildingUUID',
            'ProjectUUID',

            'CurTimeStamp',
            'BuildingNum',
            'BuildingName',
            'Unit',
            'FloorNum',
            'State',

            'House_located',
            'Pre_sale_license_number',
            'Predicted_area',
            'Measured_area',
            'Record_unit_price',
        ]
    }


class SignInfoWuhan(Document):
    RecordID = fields.UUIDField(
        default=uuid.uuid1(), binary=True, primary_key=True, null=False)
    CurTimeStamp = fields.StringField(
        default=str(datetime.datetime.now()), index=True)
    SellInfo = fields.DictField(default={'null': True}, null=True)
    meta = {
        'indexes': [
            'RecordID',
            'CurTimeStamp',
        ]
    }

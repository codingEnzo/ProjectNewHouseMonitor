# coding = utf-8
from HouseNew.models import *
from scrapy_djangoitem import DjangoItem


class ProjectBaseItem(DjangoItem):
    django_model = ProjectBaseXian


class ProjectInfoItem(DjangoItem):
    django_model = ProjectInfoXian
    fields_map = {'RecordTime': '',
                  'ProjectName': 'ProjectName',
                  'PromotionName': 'PromotionName',
                  'RealEstateProjectID': '',
                  'ProjectUUID': 'ProjectUUID',
                  'DistrictName': '',
                  'RegionName': 'ProjectCityArea',
                  'ProjectAddress': 'ProjectAddress',
                  'ProjectType': 'ProjectSupplyType',
                  'OnSaleState': 'OnSaleState',
                  'LandUse': '',
                  'HousingCount': 'ProjectTotalFlat',
                  'Developer': 'ProjectDevCompany',
                  'FloorArea': 'BuildingFloorSpace',
                  'TotalBuidlingArea': 'BuildingArea',
                  'BuildingType': '',
                  'HouseUseType': 'HouseUseType',
                  'PropertyRightsDescription': 'LandUseLife',
                  'ProjectApproveData': '',
                  'ProjectBookingData': 'ProjectBookingData',
                  'LssueDate': '',
                  'PresalePermitNumber': '',
                  'HouseBuildingCount': '',
                  'ApprovalPresaleAmount': 'ApprovalPresaleAmount',
                  'ApprovalPresaleArea': 'ApprovalPresaleArea',
                  'AveragePrice': 'AveragePrice',
                  'EarliestStartDate': '',
                  'CompletionDate': '',
                  'EarliestOpeningTime': 'EarliestOpeningDate',
                  'LatestDeliversHouseDate': 'ProjectDueDate',
                  'PresaleRegistrationManagementDepartment': '',
                  'LandLevel': '',
                  'GreeningRate': '',
                  'FloorAreaRatio': '',
                  'ManagementFees': 'PropertyCost',
                  'ManagementCompany': 'PropertyCompany',
                  'OtheRights': '',
                  'CertificateOfUseOfStateOwnedLand': '',
                  'ConstructionPermitNumber': '',
                  'QualificationNumber': '',
                  'LandUsePermit': '',
                  'BuildingPermit': '',
                  'LegalPersonNumber': '',
                  'LegalPerson': '',
                  'SourceUrl': 'ProjectInfoURL',
                  'Decoration': 'Decoration',
                  'ParkingSpaceAmount': 'ProjectParkingSpace',
                  'Remarks': '',
                  'ExtraJson': '',
                  }


class PresaleLicenseInfoItem(DjangoItem):
    django_model = PresaleInfoXian


class BuildingInfoItem(DjangoItem):
    django_model = BuildingInfoXian


class HouseInfoItem(DjangoItem):
    django_model = HouseInfoXian

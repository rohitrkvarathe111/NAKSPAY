from database import Base
from enum import Enum




class OrgCateEnum(str, Enum):
    COMPANY = "Company"
    GOVERNMENT_OFFICE = "Government Office"
    PG = "PG (Paying Guest Accommodation)"
    HOTEL = "Hotel"
    MALL = "Mall"
    CLINIC = "Clinic"
    SCHOOL = "School"


class OrgTypeEnum(str, Enum):
    PRIVATE = "Private Organization"
    PUBLIC = "Public Organization"
    GOVERNMENT = "Government Body"
    NGO = "Non-Governmental Organization"
    NON_PROFIT = "Non-Profit Organization"
    STARTUP = "Startup"
    MNC = "Multinational Corporation"
    EDUCATIONAL = "Educational Institution"
    HEALTHCARE = "Healthcare Organization"
    FINANCIAL = "Financial Institution"

class OrgIDTypeEnum(str, Enum):
    PAN = "Permanent Account Number"
    GST = "Goods and Services Tax Identification Number"
    CIN = "Corporate Identification Number"
    TAN = "Tax Deduction and Collection Account Number"
    MSME = "Micro, Small and Medium Enterprises Registration"
    UDYAM = "Udyam Registration"
    NGO_DARPAN = "NGO Darpan ID"
    FCRA = "Foreign Contribution Regulation Act Number"
    LLPIN = "Limited Liability Partnership Identification Number"



class UserTypeEnum(str, Enum):
    SUPER_ADMIN = "Super Admin"
    ORGIST_ADMIN = "Orgist Admin"
    ORGIST_USER = "Orgist User"
    USER = "User" 


class MappedStatus(str, Enum):
    PENDING = "pending"        
    ACCEPTED = "accepted"      
    REJECTED = "rejected"     
    CANCELLED = "cancelled"    
    BLOCKED = "blocked"        



class TimezoneEnum(str, Enum):
    UTC = "UTC"
    ASIA_KOLKATA = "Asia/Kolkata"
    US_EASTERN = "US/Eastern"
    US_CENTRAL = "US/Central"
    US_PACIFIC = "US/Pacific"
    EUROPE_LONDON = "Europe/London"
    EUROPE_BERLIN = "Europe/Berlin"
    AUSTRALIA_SYDNEY = "Australia/Sydney"
    ASIA_TOKYO = "Asia/Tokyo"


class IdentityTypeEnum(str, Enum):
    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    AADHAAR = "aadhaar"
    PAN = "pan"
    VOTER_ID = "voter_id"
    GREEN_CARD = "green_card"

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"



class IndiaStateEnum(str, Enum):
    ANDHRA_PRADESH = "Andhra Pradesh"
    ARUNACHAL_PRADESH = "Arunachal Pradesh"
    ASSAM = "Assam"
    BIHAR = "Bihar"
    CHHATTISGARH = "Chhattisgarh"
    GOA = "Goa"
    GUJARAT = "Gujarat"
    HARYANA = "Haryana"
    HIMACHAL_PRADESH = "Himachal Pradesh"
    JHARKHAND = "Jharkhand"
    KARNATAKA = "Karnataka"
    KERALA = "Kerala"
    MADHYA_PRADESH = "Madhya Pradesh"
    MAHARASHTRA = "Maharashtra"
    MANIPUR = "Manipur"
    MEGHALAYA = "Meghalaya"
    MIZORAM = "Mizoram"
    NAGALAND = "Nagaland"
    ODISHA = "Odisha"
    PUNJAB = "Punjab"
    RAJASTHAN = "Rajasthan"
    SIKKIM = "Sikkim"
    TAMIL_NADU = "Tamil Nadu"
    TELANGANA = "Telangana"
    TRIPURA = "Tripura"
    UTTAR_PRADESH = "Uttar Pradesh"
    UTTARAKHAND = "Uttarakhand"
    WEST_BENGAL = "West Bengal"

    # Union Territories
    ANDAMAN_NICOBAR = "Andaman and Nicobar Islands"
    CHANDIGARH = "Chandigarh"
    DADRA_NAGAR_HAVELI_DAMAN_DIU = "Dadra and Nagar Haveli and Daman and Diu"
    DELHI = "Delhi"
    JAMMU_KASHMIR = "Jammu and Kashmir"
    LADAKH = "Ladakh"
    LAKSHADWEEP = "Lakshadweep"
    PUDUCHERRY = "Puducherry"


class CountryEnum(str, Enum):
    INDIA = "India"
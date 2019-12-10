import pymongo
from gridfs import GridFS

# edb采用标准数据库还是小数据库
# 1：标准数据库；2：小数据库；
# EDB_TYPE = 2
#
# mongo-db客户端
g_mongo_client = pymongo.MongoClient("mongodb://admin:123456@192.168.182.88:27017/")

# 系统管理数据库
g_sys_manage_db = g_mongo_client["system_manage"]
# 账户集合
g_accounts_col = g_sys_manage_db["accounts"]

# firmware 数据库
g_firmware_db = g_mongo_client["firmware_share"]
# firmware 集合
g_firmware_col = g_firmware_db["firmware_share"]
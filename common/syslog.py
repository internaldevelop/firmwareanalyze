import pymysql
import uuid

from common.session import UserSession
from common.utils.general import SysUtils

# user_session = UserSession()

SUCCESS = 1
FAIL = 2
SYS_ERROR = 3
INFO = 4
EXCEPTION = 5
WARNING = 6


class SysLog:

    @staticmethod
    def add_log(type, title, contents):
        user_uuid = UserSession.get_uuid()
        mysql_db = pymysql.connect(host='192.168.182.88', user='root', password='123456', db='asset_scan', port=13306)
        cursor = mysql_db.cursor()
        # 插入数据 日志表内相应数据
        sql_insert = """insert into system_logs 
                        (uuid,type,title,contents,create_time,create_user_uuid) 
                        values('%s',%s,'%s','%s','%s','%s')""" % (
                        str(uuid.uuid4()), type, title, contents, SysUtils.get_now_time_str(), user_uuid)
        try:
            cursor.execute(sql_insert)
            # 提交事务
            mysql_db.commit()
        except Exception as e:
            # 如果异常则回滚事务
            mysql_db.rollback()
            raise e  # 可做自己想做的事
        finally:
            mysql_db.close()

        return

    @staticmethod
    def success(title, contents):
        SysLog.add_log(SUCCESS, title, contents)
        return

    @staticmethod
    def fail(title, contents):
        SysLog.add_log(FAIL, title, contents)
        return

    @staticmethod
    def sys_err(title, contents):
        SysLog.add_log(SYS_ERROR, title, contents)
        return

    @staticmethod
    def info(title, contents):
        SysLog.add_log(INFO, title, contents)
        return

    @staticmethod
    def exception(title, contents):
        SysLog.add_log(EXCEPTION, title, contents)
        return

    @staticmethod
    def warning(title, contents):
        SysLog.add_log(WARNING, title, contents)
        return

# coding=utf8
from plan.plan_config import TABLE_NAME_SUFFIX
from plan.manager import SearchConditionBeanManager
from plan.dbtools import db
import logging


class FilePipeline(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def save(self, text):
        print(text)
        try:
            with open(self.file_name, 'w') as f:
                f.write(str(text))
        except Exception:
            logging.exception()


class DBPipeline(object):
    __table_name__ = "case_plan_schema_upload_day" + TABLE_NAME_SUFFIX  # 储存数据库表名

    @staticmethod
    def proceed_manager(manager: SearchConditionBeanManager) -> SearchConditionBeanManager:
        """
        保存更新处理任务计划
        :param manager:
        :return:
        """
        if manager.node_case_num == "":
            pass

    @staticmethod
    def save(**kwargs):
        from uuid import uuid1
        schema_search = kwargs.get("schema_search")
        batch_count = kwargs.get("batch_count")
        schema_day = kwargs.get("schema_day")
        total_count = kwargs.get("total_count")
        assert schema_search
        _sql = """
        INSERT INTO {} 
          (
              rule_id,
              batch_count,
              create_date,
              update_date,
              fail,
              page_index,
              repeat_count,
              schema_day,
              schema_search,
              total_count,
              state
          ) VALUES (%s,%s ,now() ,now() ,0 ,0 ,0 ,%s ,%s ,%s ,%s)
        """.format(DBPipeline.__table_name__)
        __uuid = uuid1().__str__()
        db.insert(_sql, (__uuid, batch_count, schema_day, schema_search, total_count, "00"))

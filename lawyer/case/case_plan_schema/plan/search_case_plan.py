# coding =utf8
# ------------------添加root_path
import os
import sys

current_Path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(current_Path)[0]
__root_path = root_path.split(sep="case_plan_schema")[0]
__root_path_1 = __root_path + "context" + os.sep
__root_path_2 = __root_path + "doc" + os.sep
print(__root_path_1, "========", __root_path_2)
sys.path.append(__root_path_1)
sys.path.append(__root_path_2)
# ------------------
import logging
from util.decorator import log_cost_time
import calendar
import datetime
import time
import math
from proxy.pool import ProxyPool
from plan.pipeline import FilePipeline, DBPipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filemode='a', )
import datetime
import json
import execjs
import requests
# import tools
# from task_schema import db
from lawcase.js import wen_shu_js
from plan.manager import SearchConditionBeanManager, SearchConditionBean

import util.post_util as post_util
from util.post_util import get_random_header
from plan.plan_config import TABLE_NAME_SUFFIX

pool = ProxyPool()
pool.change_ip_proxy_cache(1)


def condition_helper(classify="裁判日期", schema_day="2018-08-09"):
    return "{}:{} TO {}".format(classify, schema_day, schema_day)


def get_between_day(begin_date, end_date):
    """
    获取从开始日期 到 结束日期 之间的范围时间
    :param begin_date:开始日期
    :param end_date:结束日期
    :return:
    """
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def init_case_plan_schema():
    schema_days = get_between_day("2001-01-06", "2006-12-31", )
    remarks = "table_name_suffix" + TABLE_NAME_SUFFIX
    logging.warning(remarks + str(schema_days))
    for schema_day in schema_days:
        # if db.exists_case_plan_schema(schema_day):
        #     continue
        while True:
            try:
                ret = init_area_court_tree(condition=condition_helper(schema_day))
                break
            except json.decoder.JSONDecodeError:
                logging.exception("JSONDecodeError")
            except requests.exceptions.ReadTimeout:
                logging.exception("ReadTimeout")
            except execjs._exceptions.ProgramError:
                logging.exception("ProgramError")
        first_count = ret[0]
        for it in ret[1:]:
            (key, value), = it.items()
            # db.insert_case_plan_schema(first_count, value, schema_day, key, table_name_suffix=TABLE_NAME_SUFFIX,
            #                            remarks=remarks)
        # db.update_case_plan_schema(schema_day, table_name_suffix=TABLE_NAME_SUFFIX, remarks=remarks)
    return False


def extract_content(param, retry=60):
    """
    获取文档目录
    :return:
    """
    while retry > 0:
        try:
            pool.validate_init_ip_proxy()
            ip_proxy_item = pool.extract_cache_ip_proxy_item()
            guid = execjs.compile(wen_shu_js).call('guid')
            referer = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=&guid="
            vjkl5 = post_util.post_get_vjkl5_url(guid, url=referer, _proxies=ip_proxy_item.proxies)
            vl5x = execjs.compile(wen_shu_js).call('getkey', vjkl5)
            number = 'wens'
            payload = {'Param': param,
                       'vl5x': vl5x,
                       'guid': guid,
                       'number': number,
                       }
            headers = {'Accept': '*/*',
                       'Accept-Encoding': 'gzip, deflate',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Connection': 'keep-alive',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'Host': 'wenshu.court.gov.cn',
                       'Origin': 'http://wenshu.court.gov.cn',
                       'Cookie': 'vjkl5=' + vjkl5,
                       'User-Agent': get_random_header(),
                       'X-Requested-With': 'XMLHttpRequest',
                       }
            logging.info(payload)
            logging.info(headers)
            ret = requests.post(url='http://wenshu.court.gov.cn/List/TreeContent', data=payload, headers=headers,
                                proxies=ip_proxy_item.proxies,
                                timeout=25)
            assert ret.status_code == 200
            assert ret.json()
            json_text = ret.json()
            ret.close()
            logging.info(json_text)
            ip_proxy_item.success()
            return json_text
        except requests.exceptions.ProxyError:
            ip_proxy_item.fail(multiple=5)
            logging.exception("=*= 错误发生还剩 {} 次 =*=".format(str(retry)))
        except execjs._exceptions.ProgramError:
            ip_proxy_item.fail(multiple=2)
            logging.exception("=*= 错误发生还剩 {} 次 =*=".format(str(retry)))
        except Exception:
            logging.exception("=*= 错误发生还剩 {} 次 =*=".format(str(retry)))
            ip_proxy_item.fail()
            time.sleep(1)
            retry = retry - 1


def partition_context(manager: SearchConditionBeanManager, only_year=False):
    """
    裁判年份-条件分片
    :param param: 上一个条件
    :return:
    """
    # manager = SearchConditionBeanManager.build(param)
    if manager.child_node:  # 如果有子节点,不加载
        return manager
    if manager.is_load_case():
        return manager
    if only_year and "裁判日期" in manager.str():
        return manager
    param = manager.str()
    json_text = extract_content(param)
    json_data = json.loads(json_text)
    for it in json_data:
        if it.get("Key") == "裁判年份":  #
            child = it.get("Child")
            int_value = it.get("Value")
            manager.node_case_num = int(int_value)
            logging.info(manager)
            for _child_it in child:
                _child_key = _child_it.get("Key")
                _child_value = _child_it.get("Value")
                _child_field = _child_it.get("Field")
                if _child_key == "":
                    continue
                _child_value = int(_child_value)
                if _child_value == 0:  # 没有值,do nothing
                    continue
                if manager.priority() and not manager.priority_proceed():
                    sub_manager = SearchConditionBeanManager.build(param)
                    bean = SearchConditionBean(name=_child_field, value=[_child_key])
                    sub_manager.append_bean(bean)
                    sub_manager.node_case_num = _child_value
                    manager.child_node.append(sub_manager)
            break
        else:
            continue
    return manager


def proceed_court_tree_context(condition="裁判日期:2018-09-01 TO 2018-09-01", field="", key="", value="", ret_context=[]):
    """

    :param condition:大类业务条件：当天日期截取
    :param field:
    :param key:增加条件
    :param value:
    :param ret_context:保存搜索算法容器
    :return:
    """
    param = "{},{}:{}".format(condition, field, key)
    json_text = __proceed_court_tree_context(param, key)
    logging.info(json_text)
    _value = 0
    try:
        json_var = json.loads(json_text)
    except Exception:
        logging.error(json_text)
        try:
            _value = int(value)
        except Exception as e:
            logging.exception("Exception")
        ret_context.append({"{},{}:{}".format(condition, field, key): _value})
        return
    count = int(json_var[0].get("IntValue"))
    if count <= 0:
        logging.info("{} 条件舍弃未有文书".format(param))
        ret_context.append({"{},{}:{}".format(condition, field, key): int(value)})
        return
    elif count <= 200:
        ret_context.append({param: count})  # 统计算法数，理论存在文档数
    else:
        _data = json_var[0].get("Child")
        _length = len(_data)  # 数据长度
        for index, it in enumerate(_data):
            _key = it.get("Key")
            _int_value = it.get("IntValue")
            _field = it.get("Field")
            if _key == "" or _int_value == 0:
                continue
            if _int_value <= 200:
                ret_context.append({"{},{}:{}".format(condition, _field, _key): _int_value})
                continue
            else:
                if (index - 1) > 0 and "此节点加载中" in _data[index - 1].get("Value"):
                    proceed_court_tree_context(condition, _field, _key, value, ret_context)
                else:
                    ret_context.append({"{},{}:{}".format(condition, _field, _key): _int_value})


def __proceed_court_tree_context(param, parval, retry=60):
    payload = {'Param': param,
               'parval': parval,
               }
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Host': 'wenshu.court.gov.cn',
               'Origin': 'http://wenshu.court.gov.cn',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1471.813 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               }
    pool.validate_init_ip_proxy()
    ip_proxy_item = pool.extract_cache_ip_proxy_item()
    proxies = ip_proxy_item.proxies
    logging.info(payload)
    logging.info(headers)
    success = False
    count = 0
    json_text = ""
    while not success:
        if count >= retry:
            raise Exception("超过重试次数")
        count += 1
        try:
            ret = requests.post(url='http://wenshu.court.gov.cn/List/CourtTreeContent', data=payload, headers=headers,
                                proxies=proxies,
                                timeout=15)
            assert ret.status_code == 200
            json_text = ret.json()
            ret.close()
        except requests.exceptions.ProxyError:
            ip_proxy_item.fail(multiple=5)
            logging.exception("=*= 错误发生还剩 {} 次 =*=".format(str(retry - count)))
        except execjs._exceptions.ProgramError:
            ip_proxy_item.fail(multiple=2)
            logging.exception("=*= 错误发生还剩 {} 次 =*=".format(str(retry - count)))
        except Exception:
            ip_proxy_item.fail()
            logging.exception("error==>")
        if "Key" in json_text:
            success = True
        else:
            logging.warning("重试->" + str(count) + str(payload))
    return json_text


def init_court_tree(condition="裁判日期:2018-08-09 TO 2018-08-09"):
    json_text = extract_content(condition)
    json_data = json.loads(json_text)
    ret_context = []
    for it in json_data:
        print(it)
        if it.get("Key") == "法院地域":  #
            child = it.get("Child")
            int_value = it.get("IntValue")
            ret_context.append(int_value)
            for _child_it in child:
                _child_key = _child_it.get("Key")
                _child_value = _child_it.get("Value")
                _child_field = _child_it.get("Field")
                if _child_key == "":
                    continue
                _child_value = int(_child_value)
                if _child_value == 0:  # 没有值,do nothing
                    continue
                if _child_value <= 200:
                    ret_context.append({"{},{}:{}".format(condition, _child_field, _child_key): _child_value})
                    continue
                proceed_court_tree_context(condition, _child_field, _child_key, _child_value,
                                           ret_context, )
            break
        else:
            continue
    return ret_context


def init_case_plan_schema_day(start_day, end_day, table_name_suffix, classify):
    """
    :param start_day:"2001-01-06"
    :param end_day:"2006-12-31"
    :return:
    """
    schema_days = get_between_day(start_day, end_day)
    remarks = "table_name_suffix" + table_name_suffix
    logging.warning(remarks + str(schema_days))
    for schema_day in schema_days:
        # if db.exists_case_plan_schema(schema_day, table_name_suffix=table_name_suffix):
        #     continue
        while True:
            try:
                ret = init_area_court_tree(condition=condition_helper(schema_day=schema_day, classify=classify))
                break
            except json.decoder.JSONDecodeError:
                logging.exception("JSONDecodeError")
            except requests.exceptions.ReadTimeout:
                logging.exception("ReadTimeout")
            except execjs._exceptions.ProgramError:
                logging.exception("ProgramError")
        first_count = ret[0]
        for it in ret[1:]:
            (key, value), = it.items()
            # db.insert_case_plan_schema(first_count, value, schema_day, key, table_name_suffix=table_name_suffix,
            #                            remarks=remarks)
        # db.update_case_plan_schema(schema_day, table_name_suffix=table_name_suffix, remarks=remarks)
    return False


def proceed_referee_partition_context(manager: SearchConditionBeanManager):
    """
    裁判日期-遍历数据
    :param manager:
    :return:
    """
    assert isinstance(manager, SearchConditionBeanManager)
    __child_node = manager.child_node
    __node_case_num = manager.node_case_num
    if __child_node:
        for __manager in __child_node:
            proceed_referee_partition_context(__manager)
    elif __node_case_num > 200:
        __proceed_partition_context(manager)
    return manager


def proceed_area_partition_context(manager: SearchConditionBeanManager):
    """
    裁判地域法院-遍历数据
    :param manager:
    :return:
    """
    assert isinstance(manager, SearchConditionBeanManager)
    __child_node = manager.child_node
    __node_case_num = manager.node_case_num
    if __child_node:
        for __manager in __child_node:
            proceed_area_partition_context(__manager)
    elif __node_case_num > 200:
        if manager.is_range_end_point(query_bean_type="裁判日期"):
            init_area_court_tree(manager)
        logging.warning("=*= proceed_area_partition_context跳过：{} $ {} =*=".format(str(__node_case_num), manager.str()))
    return manager


def init_area_court_tree(manager: SearchConditionBeanManager):
    """
    初始化地区法院
    :param condition:
    :return:
    """
    json_text = extract_content(manager.str())
    json_data = json.loads(json_text)
    ret_context = []
    for it in json_data:
        print(it)
        if it.get("Key") == "法院地域":  #
            child = it.get("Child")
            int_value = it.get("IntValue")
            ret_context.append(int_value)
            for _child_it in child:
                _child_key = _child_it.get("Key")
                _child_value = _child_it.get("Value")
                _child_field = _child_it.get("Field")
                if _child_key == "":
                    continue
                _child_value = int(_child_value)
                if _child_value == 0:  # 没有值,do nothing
                    continue
                if _child_value <= 200:
                    ret_context.append({"{},{}:{}".format(manager.str(), _child_field, _child_key): _child_value})
                    continue
                proceed_court_tree_context(manager.str(), _child_field, _child_key, _child_value,
                                           ret_context, )
            break
        else:
            continue
    print(ret_context)
    if ret_context:
        for data in ret_context:
            if isinstance(data, dict) and data:
                key, value = data.popitem()
                print(key, value)
                sub_manager = manager.build(key)
                sub_manager.node_case_num = value
                manager.child_node.append(sub_manager)
    return manager


def days(str1, str2):
    """
    计算日期相隔的天数
    :param str1:
    :param str2:
    :return:
    """
    date1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d")
    num = (date2 - date1).days
    return num


def transfer_date(time_str: str):
    _date = datetime.datetime.strptime(time_str[0:10], "%Y-%m-%d")
    return _date


def __proceed_partition_context(manager: SearchConditionBeanManager):
    """
    计算案例分布时间,一直切割条件
    :param case_num:案例数量
    :param year:年份
    :param key:key值
    :return:
    """
    assert len(manager.child_node) == 0
    if manager.is_range_end_point("裁判日期"):
        logging.warning("=*=__proceed_partition_context跳过: {} =*=".format(manager.str()))
        return
    __priority = manager.priority()
    if not __priority:
        __priority = "裁判日期"
    match = False
    for data in manager.beans:
        if "裁判日期" in data.name:
            start_time = data.value[0]
            end_time = data.value[1]
            match = True
            continue
    # 裁判年份:2014
    if not match:
        value = manager.query_bean_value_by("裁判年份")
        if value and isinstance(value, list):
            start = int(value[0])
            end = start + 1
            __format = "{}-01-01"
            start_time = __format.format(start)
            end_time = __format.format(end)

    __days = days(start_time, end_time)
    __pear_case = math.ceil(manager.node_case_num / 200)
    __partition = __days // __pear_case - 1
    print(__partition)
    if __partition < 0:
        __partition = 0
    time_partition_list = []
    begain = transfer_date(start_time)  # 开始时间
    end = transfer_date(end_time)  # 结束时间
    _step = begain  # 偏移结束时间
    while end >= _step:
        _before_step = _step
        _step = _step + datetime.timedelta(days=__partition)  # 偏移结束时间
        if _step > end:
            _step = end
        _before_step_time = _before_step.strftime("%Y-%m-%d")
        _step_time = _step.strftime("%Y-%m-%d")
        bean = SearchConditionBean(name=__priority, value=[_before_step_time, _step_time])
        _step = _step + datetime.timedelta(days=1)  # 下一次开始时间
        time_partition_list.append(bean)
    for time_partition in time_partition_list:
        sub_manager = SearchConditionBeanManager.build(manager.str())
        sub_manager.append_bean(time_partition)
        manager.child_node.append(sub_manager)
    logging.info(manager)


def partition_load_node_case_num(manager: SearchConditionBeanManager):
    """
    加载每片的数量
    :param manager:
    :return:
    """
    if not manager.is_load_case():
        partition_context(manager, )
    elif manager.child_node:
        for __manager in manager.child_node:
            partition_load_node_case_num(__manager)
    return manager


# _test = SearchConditionBeanManager.build("上传日期:2018-11-12 TO 2018-11-12,基层法院:南京市鼓楼区人民法院,裁判年份:2014")
# _test.node_case_num = 2857
# proceed_referee_partition_context(_test)
file_pipeline = FilePipeline("C:/Users/Administrator/PycharmProjects/{}".format("test.text"))
manager = SearchConditionBeanManager.build(
    "上传日期:2018-11-01 TO 2018-11-01")
while not manager.is_complete():
    partition_context(manager, only_year=True)  # 裁判年份
    proceed_referee_partition_context(manager)  # 裁downloadBillOrder判日期
    partition_load_node_case_num(manager)  # 加载未有的案例
    proceed_area_partition_context(manager)  # 法院地域

partition_list = manager.partition_list()
ret = []
for partition in partition_list:
    schema_search_str = partition.str()
    __data = {'schema_search': schema_search_str, 'batch_count': partition.node_case_num,
              'schema_day': schema_search_str[
                            schema_search_str.index("上传日期:") + 5:schema_search_str.index("上传日期:") + 15],
              'total_count': manager.node_case_num}
    ret.append(__data)
for it in ret:
    DBPipeline.save(**it)

# print(manager)
# json_text = partition_context("上传日期:2018-11-12 TO 2018-11-12,基层法院:南京市鼓楼区人民法院,裁判年份:2014")

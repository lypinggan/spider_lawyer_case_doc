class SearchConditionBean(object):
    """
    搜索条件
    """
    __range_format = "{}:{} TO {}"  # 时间区间
    __str_format = "{}:{}"  #

    def __init__(self, name, value: list):
        """
        条件初始化
        :param name:条件名字
        :param value:条件值
        :param range:是否是区间值
        """
        self.name = name
        self.value = value
        self.int_value = 0
        self.range_end_point = False
        assert len(value) >= 1
        if len(value) == 1:
            self.range = False
        else:
            self.range = True
            if value[0] == value[1]:
                self.range_end_point = True

    def str_condition(self):
        __ret = ""
        if self.range:
            __ret = self.__range_format.format(self.name, self.value[0], self.value[1])
        else:
            __ret = self.__str_format.format(self.name, self.value[0])
        return __ret

    def set_int_value(self, int_value):
        self.int_value = int_value

    def __str__(self):
        return self.str_condition()

    def __repr__(self):
        return self.__str__()


class SearchConditionBeanManager(object):
    _priority = {"裁判年份": False, "裁判日期": True}
    _seperate = ","  # 分割字符
    DEAULT_NODE_CASE_NUM = -1
    _max_case_count = 200

    def __init__(self, beans: list):
        self.child_node = []  # 是否有子节点
        self.node_case_num = self.DEAULT_NODE_CASE_NUM  # 该节点的案例数
        self.beans = beans

    def is_range_end_point(self, query_bean_type):
        _range_end_point = False
        for bean in self.beans:
            assert isinstance(bean, SearchConditionBean)
            if query_bean_type == bean.name and bean.range and bean.range_end_point:
                _range_end_point = True
        return _range_end_point

    def is_load_case(self):
        """
        是否有加载过
        :return:
        """
        return self.node_case_num != self.DEAULT_NODE_CASE_NUM

    def is_complete(self):
        """
        是否完成了分割
        :return:
        """
        complete = False
        if self.node_case_num == self.DEAULT_NODE_CASE_NUM:
            return complete
        if self.child_node:
            for data in self.child_node:
                assert isinstance(data, SearchConditionBeanManager)
                if not data.is_complete():
                    return complete
        elif self.node_case_num > 200:  # 继续细分
            if not self.is_range_end_point(query_bean_type="裁判日期"):  # 无法再细分
                return complete
        complete = True
        return complete

    def str(self):
        '''
        搜索条件字符串
        :param beans:条件集
        :return:
        '''
        if self.beans:
            __ret_str = ""
            for bean in self.beans:
                assert isinstance(bean, SearchConditionBean)
                seperate = ""
                if __ret_str:  # 不是第一个元素
                    seperate = self._seperate
                __ret_str += seperate + bean.str_condition()
            return __ret_str

    @staticmethod
    def build(string_condition):
        if string_condition:
            __ret = []
            __str_list = string_condition.split(sep=SearchConditionBeanManager._seperate)
            for __str in __str_list:
                __sub_str_list = __str.split(":")
                print(__sub_str_list)
                if " TO " in __sub_str_list[1]:
                    __range_str_list = __sub_str_list[1].split(sep=" TO ")
                    __ret.append(
                        SearchConditionBean(name=__sub_str_list[0], value=[__range_str_list[0], __range_str_list[1]]))
                else:
                    __ret.append(SearchConditionBean(name=__sub_str_list[0], value=[__sub_str_list[1]]))
            _manager = SearchConditionBeanManager(__ret)
            return _manager

    def partition_list(self) -> list:
        assert self.is_complete()
        __ret_list = []
        if self.child_node:
            for child in self.child_node:
                __child_ret_list = child.partition_list()
                __ret_list = __ret_list + __child_ret_list
        else:
            __ret_list.append(self)
        return __ret_list

    def append_bean(self, bean):
        assert isinstance(bean, SearchConditionBean)
        update = False
        for data in self.beans:
            if bean.name in data.name:
                data.value = bean.value
                update = True
        if not update:
            self.beans.append(bean)

    def query_bean_value_by(self, name):
        for bean in self.beans:
            if name in bean.name:
                return bean.value
        return []

    def priority(self):
        for (key, value) in self._priority.items():
            if key not in self.str():
                return key

    def priority_proceed(self):
        """
        是否继续执行:True,还可以继续获取页数
        :return:
        """
        if self.priority():
            return self._priority[self.priority()]

    def __str__(self):
        if len(self.child_node) == 0:
            templete = """node_case_num={} beans_str={} child_node={}"""
        else:
            templete = """node_case_num={} beans_str={} child_node={}
"""
        return templete.format(str(self.node_case_num), self.str(),
                               str(self.child_node))

    def __repr__(self):
        return self.__str__()

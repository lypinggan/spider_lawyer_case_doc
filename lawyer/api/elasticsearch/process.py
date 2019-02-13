# coding=utf-8
import re


class Classifier(object):
    """
    分类器
    """

    def __init__(self, doc):
        """
        :param doc: 未加工原料
        """
        self.doc = doc

    def process(self):
        raise NotImplementedError("Classifier没有实现")


class Lawyer(object):
    def __init__(self, lawyer_name, law_firm):
        self.lawyer_name = lawyer_name
        self.law_firm = law_firm

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class Party(object):
    """
    当事人
    """
    TYPE_原告 = "原告"
    TYPE_被告 = "被告"

    def __init__(self, name, type=""):
        self.name = name

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class LawyerClassifier(Classifier):
    """
    律师分类
    """

    def __init__(self, doc):
        super().__init__(doc)
        self.data = []

    def process(self):
        if self.doc:
            _data_list = re.findall(r'委托代理人：([\s\S]*?)事务所', doc)
            _ret = []
            for data in _data_list:
                _data = data.split("，")
                _ret.append(Lawyer(lawyer_name=_data[0], law_firm="{}事务所".format(_data[2])))
            self.data = _ret


with open("./h5.html", encoding="utf-8") as f:
    doc = f.read()
cf = LawyerClassifier(doc)
cf.process()
# print(cf.data)

#!/usr/bin/env python
# coding=utf-8

"""

@author: sml2h3

@license: (C) Copyright 2018-2020

@contact: sml2h3@gmail.com

@software: mmewmd_crack_for_wenshu

@file: encrypt

@time: 2019-01-17
"""

import execjs
import requests
from lxml import etree
import re
import uuid
import os

prd = os.path.dirname(os.path.abspath(__file__))
print(prd)
with open(prd + './vl5x.js', 'r', encoding="utf-8") as fp:
    js = fp.read()
with open(prd + './encrypt.js', 'r', encoding="utf-8") as f:
    js1 = f.read()
with open(prd + './ywtu.js', 'r', encoding="utf-8") as f:
    js2 = f.read()


def build_mmewmd():
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "ccpassport=1ff98c661b8f424096c234ce889da9b0;_gscu_2116842793=47626758817stt18; _gscs_2116842793=47659453ttzz3o20|pv:14; _gscbrs_2116842793=1; wzwsconfirm=0e561c10c60c2f0d44410644eb3c2403; wzwstemplate=NQ==; wzwschallenge=-1;wzwsvtime=1547659451;",
        "Host": "wenshu.court.gov.cn",
        "Origin": "http://wenshu.court.gov.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    url = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6"
    rsp = requests.get(url, headers=headers)
    f80s = rsp.cookies['FSSBBIl1UgzbN7N80S']
    f80t = rsp.cookies['FSSBBIl1UgzbN7N80T']
    ctx1 = execjs.compile(js1)
    ctx2 = execjs.compile(js2)
    html = etree.HTML(rsp.text)
    meta = html.xpath('//*[@id="9DhefwqGPrzGxEp9hPaoag"]/@content')[0]
    ywtu = ctx2.call("getc", meta)
    f80t_n = ctx1.call("getCookies", meta, f80t, ywtu)
    return f80s, f80t_n


def build_uuid():
    _id = uuid.uuid4().__str__().split("-")
    _uuid = "{}-{}-{}{}-{}".format(*_id)
    return _uuid


def get_vl5x(vjkl5):
    """
    根据vjkl5获取参数vl5x
    """
    ctx = execjs.compile(js)
    vl5x = (ctx.call('GetVl5x', vjkl5))
    return vl5x


async def extract_mmd_param(client, _proxies) -> dict:
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "ccpassport=1ff98c661b8f424096c234ce889da9b0;_gscu_2116842793=47626758817stt18; _gscs_2116842793=47659453ttzz3o20|pv:14; _gscbrs_2116842793=1; wzwsconfirm=0e561c10c60c2f0d44410644eb3c2403; wzwstemplate=NQ==; wzwschallenge=-1;wzwsvtime=1547659451;",
        "Host": "wenshu.court.gov.cn",
        "Origin": "http://wenshu.court.gov.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    writ_content = await client.get(
        url="http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6",
        proxy_headers=headers,
        timeout=15,
        proxy=_proxies.get("http"),
    )
    retry = 4
    if retry > 0:
        html_text = await writ_content.text()
        html = etree.HTML(html_text)
        f80s = writ_content.cookies['FSSBBIl1UgzbN7N80S']
        f80s = re.findall('FSSBBIl1UgzbN7N80S=(.*?);', str(f80s))[0]
        f80t = writ_content.cookies['FSSBBIl1UgzbN7N80T']
        f80t = re.findall('FSSBBIl1UgzbN7N80T=(.*?);', str(f80t))[0]
        ctx1 = execjs.compile(js1)
        ctx2 = execjs.compile(js2)
        meta = html.xpath('//*[@id="9DhefwqGPrzGxEp9hPaoag"]/@content')[0]
        ywtu = ctx2.call("getc", meta)
        f80t_n = ctx1.call("getCookies", meta, f80t, ywtu)
        _ret = {"FSSBBIl1UgzbN7N80S": f80s, "FSSBBIl1UgzbN7N80T": f80t_n}
        print(_ret)
        if writ_content:
            writ_content.close()
        return _ret


def main():
    doc_id = "8d39d696-e030-4eac-8870-a9d00033bce9"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "FSSBBIl1UgzbN7N80S={}; FSSBBIl1UgzbN7N80T={};".format(
            *build_mmewmd()),
        "Host": "wenshu.court.gov.cn",
        "Origin": "http://wenshu.court.gov.cn",
        "Referer": "http://wenshu.court.gov.cn/content/content?DocID={}&KeyWord=".format(doc_id),
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    data = {
        "DocID": "{}".format(doc_id),
    }
    url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}".format(doc_id)
    rsp = requests.post(url, headers=headers, data=data)
    print(rsp.text)

[

]
if __name__ == "__main__":
    with open(prd + './doc_id.data', 'r', encoding="utf-8") as fp:
        data = fp.read()
    print(data.split('\\n'))
    # main()

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
import time
import logging
import aiohttp
import asyncio

prd = os.path.dirname(os.path.abspath(__file__))
print(prd)
with open(prd + '/vl5x.js', 'r', encoding="utf-8") as fp:
    js = fp.read()
with open(prd + '/encrypt.js', 'r', encoding="utf-8") as f:
    js1 = f.read()
with open(prd + '/ywtu.js', 'r', encoding="utf-8") as f:
    js2 = f.read()


class InvalidIP(Exception):
    """
    无效的IP.
    """

    def __init__(self, code=999, msg=""):
        self.code = code
        self.msg = msg


class Context(object):

    def __init__(self, meta, f80t, ywtu):
        self.meta = meta
        self.f80t = f80t
        self.ywtu = ywtu
        ctx1 = execjs.compile(js1)
        self.f80t_n = ctx1.call("getCookies", meta, f80t, ywtu)

    def fresh(self):
        pass


async def build_mmewmd(ip_proxy_item=None):
    try:
        if hasattr(ip_proxy_item, "cookies") and ip_proxy_item.recent_fail_count == 0:  # 失败了
            cookies = ip_proxy_item.cookies
        else:
            cookies = {
                "ccpassport": "1ff98c661b8f424096c234ce889da9b0",
                "_gscu_2116842793": "47626758817stt18",
                "_gscs_2116842793": "47659453ttzz3o20|pv:14",
                "_gscbrs_2116842793": "1",
                "wzwsconfirm": "0e561c10c60c2f0d44410644eb3c2403",
                "wzwstemplate": "NQ==",
                "wzwschallenge": "-1",
                "wzwsvtime": ""
            }
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "wenshu.court.gov.cn",
            "Origin": "http://wenshu.court.gov.cn",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        url = "http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+%E4%BA%91%E5%8D%97%E4%B8%87%E6%88%90%E5%BE%8B%E5%B8%88%E4%BA%8B%E5%8A%A1%E6%89%80+LS++%E5%BE%8B%E6%89%80:%E4%BA%91%E5%8D%97%E4%B8%87%E6%88%90%E5%BE%8B%E5%B8%88%E4%BA%8B%E5%8A%A1%E6%89%80&conditions=searchWord+%E9%87%91%E5%88%99%E8%BE%89+LAWYER++%E5%BE%8B%E5%B8%88:%E9%87%91%E5%88%99%E8%BE%89"

        proxy = ip_proxy_item.proxies if isinstance(ip_proxy_item.proxies, str) else ip_proxy_item.proxies.get("http")
        cookies['wzwsvtime'] = str(int(time.time()))
        if hasattr(ip_proxy_item, "cookies") and ip_proxy_item.recent_fail_count == 0:
            cookies['FSSBBIl1UgzbN7Nenable'] = "true"
            ctx1 = execjs.compile(js1)
            cookies["FSSBBIl1UgzbN7N80T"] = ctx1.call("getCookies",
                                                      ip_proxy_item.meta,
                                                      ip_proxy_item.f80t,
                                                      ip_proxy_item.ywtu
                                                      )
            # ip_proxy_item.f80t = cookies["FSSBBIl1UgzbN7N80T"]
            ip_proxy_item.cookies = cookies
            print("------使用了旧cookies------")
            return cookies
        async with aiohttp.ClientSession() as client:
            rsp = await client.get(
                url=url,
                proxy_headers=headers,
                timeout=10,
                proxy=proxy,
            )
            html_text = await rsp.text()
            html = etree.HTML(html_text)
            cookies['wzwsvtime'] = str(int(time.time()))
            f80s = rsp.cookies['FSSBBIl1UgzbN7N80S']
            f80s = re.findall('FSSBBIl1UgzbN7N80S=(.*?);', str(f80s))[0]
            f80t = rsp.cookies['FSSBBIl1UgzbN7N80T']
            f80t = re.findall('FSSBBIl1UgzbN7N80T=(.*?);', str(f80t))[0]
            ctx1 = execjs.compile(js1)
            ctx2 = execjs.compile(js2)
            meta = html.xpath('//*[@id="9DhefwqGPrzGxEp9hPaoag"]/@content')[0]
            ywtu = ctx2.call("getc", meta)
            f80t_n = ctx1.call("getCookies", meta, f80t, ywtu)
            cookies["FSSBBIl1UgzbN7N80S"] = f80s
            cookies["FSSBBIl1UgzbN7N80T"] = f80t_n

            ip_proxy_item.meta = meta
            ip_proxy_item.f80t = f80t
            ip_proxy_item.ywtu = ywtu
            # ip_proxy_item.cookies = cookies
            return cookies
    except Exception as e:
        logging.exception(e)
        raise InvalidIP(code=999, msg="获取f80s f80t_n出错了.")


def build_uuid():
    _id = uuid.uuid4().__str__().split("-")
    _uuid = "{}-{}-{}{}-{}".format(*_id)
    return _uuid


def get_vl5x(vjkl5):
    """
    根据vjkl5获取参数vl5x
    """
    ctx = execjs.compile(js)
    vl5x = (ctx.call('getKey', vjkl5))
    return vl5x


async def extract_mmd_param(cookies, _proxies, url, context) -> dict:
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "wenshu.court.gov.cn",
        "Origin": "http://wenshu.court.gov.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    cookies['wzwsvtime'] = str(int(time.time()))
    async with aiohttp.ClientSession(cookies=cookies) as client:
        proxy = _proxies if isinstance(_proxies, str) else _proxies.get("http")
        writ_content = await client.post(
            url=url,
            headers=headers,
            timeout=15,
            proxy=proxy,
        )
        html_text = await writ_content.text()
        html = etree.HTML(html_text)
        f80s = writ_content.cookies['FSSBBIl1UgzbN7N80S']
        f80s = re.findall('FSSBBIl1UgzbN7N80S=(.*?);', str(f80s))[0]
        context["f80s"] = f80s
        f80t = writ_content.cookies['FSSBBIl1UgzbN7N80T']
        f80t = re.findall('FSSBBIl1UgzbN7N80T=(.*?);', str(f80t))[0]
        context["f80t"] = f80t
        ctx1 = execjs.compile(js1)
        ctx2 = execjs.compile(js2)
        meta = html.xpath('//*[@id="9DhefwqGPrzGxEp9hPaoag"]/@content')[0]
        context["meta"] = meta
        ywtu = ctx2.call("getc", meta)
        context["ywtu"] = ywtu
        if writ_content:
            writ_content.close()

    # step2:获取vjkl5
    ywtu = ctx2.call("getc", meta)
    context["ywtu"] = ywtu
    f80t_n = ctx1.call("getCookies", meta, f80t, ywtu)
    cookies['FSSBBIl1UgzbN7Nenable'] = "true"
    cookies['FSSBBIl1UgzbN7N80S'] = f80s
    cookies['FSSBBIl1UgzbN7N80T'] = f80t_n
    cookies['wzwsvtime'] = str(int(time.time()))
    async with aiohttp.ClientSession(cookies=cookies) as client:
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "wenshu.court.gov.cn",
            "Origin": "http://wenshu.court.gov.cn",
            "Referer": "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        writ_content = await client.post(url=url,
                                         headers=headers,
                                         timeout=10,
                                         proxy=proxy,
                                         )
        ret_text = await writ_content.text()
        assert writ_content.status == 200
        vjkl5 = writ_content.cookies.get("vjkl5")
        vjkl5 = re.findall('vjkl5=(.*?);', str(vjkl5))[0]
        context["vjkl5"] = vjkl5
        f80t_n = ctx1.call("getCookies", meta, f80t, ywtu)
        context["f80t_n"] = f80t_n
        logging.warning("vjkl5=" + vjkl5)
        if writ_content:
            writ_content.close()
        return context


async def main(doc_id, ip_proxy_item):
    proxies = ip_proxy_item.proxies
    cookies = await build_mmewmd(ip_proxy_item)
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "FSSBBIl1UgzbN7N80S={}; FSSBBIl1UgzbN7N80T={};".format(cookies.get("FSSBBIl1UgzbN7N80S"),
                                                                         cookies.get("FSSBBIl1UgzbN7N80T")),
        "Host": "wenshu.court.gov.cn",
        "Origin": "http://wenshu.court.gov.cn",
        "Referer": "http://wenshu.court.gov.cn/content/content?DocID={}&KeyWord=".format(doc_id),
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    data = {
        "DocID": "{}".format(doc_id),
    }
    url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}".format(doc_id)

    # rsp = requests.post(url, headers=headers, data=data, proxies=proxies)  # TODO:
    # print(rsp.text)
    # return rsp.text
    proxy = ip_proxy_item.proxies if isinstance(ip_proxy_item.proxies, str) else ip_proxy_item.proxies.get("http")
    async with aiohttp.ClientSession() as client:
        rsp = await client.post(
            url=url,
            headers=headers,
            data=data,
            timeout=10,
            proxy=proxy,
        )
        html_text = await rsp.text()
        if rsp.status != 200:
            logging.error("=====rsp.status={}".format(rsp.status))
        assert rsp.status == 200
        print(html_text)
        return html_text


proxies = {
    "http": "http://125.87.105.151:33044",
}
# proxy = {"http": "http://222.219.69.216:15442"}

if __name__ == "__main__":
    with open(prd + './doc_id.data', 'r', encoding="utf-8") as fp:
        for line in fp.readlines():
            print(line.strip())
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                asyncio.wait(
                    [main(line.strip(), proxies)])
            )
            time.sleep(1)
    # print(data.split('\\n'))
    # main("8d39d696-e030-4eac-8870-a9d00033bce9")

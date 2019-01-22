# coding=utf-8
from proxy.pool import ProxyPool
import logging
import re


async def async_post_get_vjkl5_url(client, guid, proxies={}, cookies={}):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "FSSBBIl1UgzbN7N80S={}; FSSBBIl1UgzbN7N80T={}; ccpassport=1ff98c661b8f424096c234ce889da9b0;_gscu_2116842793=47626758817stt18; _gscs_2116842793=47659453ttzz3o20|pv:14; _gscbrs_2116842793=1; wzwsconfirm=0e561c10c60c2f0d44410644eb3c2403; wzwstemplate=NQ==; wzwschallenge=-1;wzwsvtime=1547659451;".format(
            cookies.get("FSSBBIl1UgzbN7N80S"), cookies.get("FSSBBIl1UgzbN7N80T")),
        "Host": "wenshu.court.gov.cn",
        "Origin": "http://wenshu.court.gov.cn",
        "Referer": "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }
    print(headers)
    url = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6"
    writ_content = await client.get(url=url,
                                    proxy_headers=headers,
                                    timeout=10,
                                    proxy=proxies.get("http"),
                                    )
    ret_text = await writ_content.text()
    print(ret_text)
    print(writ_content.cookies)
    print(writ_content.status)
    assert writ_content.status == 200
    vjkl5 = writ_content.cookies.get("vjkl5")
    _ret = re.findall('vjkl5=(.*?);', str(vjkl5))[0]
    logging.info("vjkl5=" + _ret)
    if writ_content:
        writ_content.close()
    return _ret


async def post_list_context_by_param(client, guid, vjkl5, vl5x, number, param, index=1, page=20, _proxies={},
                                     cookies={}):
    from lawcase.config import LIST_CONTEXT_ORDER_BY, LIST_CONTEXT_ORDER_DIRECTION
    client.cookie_jar.clear()
    payload = {'Param': param,
               'Index': index,
               'Page': page,
               'Order': LIST_CONTEXT_ORDER_BY,
               'Direction': LIST_CONTEXT_ORDER_DIRECTION,
               'vl5x': vl5x,
               'number': number,
               'guid': guid,
               }
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               "Cookie": "FSSBBIl1UgzbN7N80S={};FSSBBIl1UgzbN7N80T={};vjkl5={};".format(
                   cookies.get("FSSBBIl1UgzbN7N80S"),
                   cookies.get("FSSBBIl1UgzbN7N80T"),
                   cookies.get("vjkl5"),
               ),
               'Host': 'wenshu.court.gov.cn',
               'Origin': 'http://wenshu.court.gov.cn',
               'Referer': 'http://wenshu.court.gov.cn/list/list/?sorttype=1&number=&guid=' + guid,
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1471.813 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               }
    logging.info("*=*== _proxies=" + str(_proxies) + ";param=" + param + ";index=" + str(index) + " *=*==")
    _ret = await client.post(url='http://wenshu.court.gov.cn/List/ListContent',
                             proxy_headers=headers,
                             data=payload,
                             timeout=15,
                             proxy=_proxies.get("http"),
                             )
    assert _ret.status == 200
    ret_text = await _ret.text()
    if _ret:
        _ret.close()
    return ret_text

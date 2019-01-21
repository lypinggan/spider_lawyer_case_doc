# coding=utf8
import logging
import sys
import re
import time
import os
import execjs
from util.decorator import log_cost_time

current_Path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(current_Path)[0]
print(root_path)
sys.path.append(root_path)
__all__ = ["get_linux_time", "decrypt_id", "_test", "_value1"]
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S', filemode='a', )
logging.info(execjs.get().name)
with open(root_path + "/js/list_context_parser_2018_12_21.js") as f:
    doc_id_js = f.read()


def get_linux_time():
    """
    获取linux 10位时间戳
    :return:
    """
    return time.time().__int__()


_test = "w61ZS27CgzAQPQtRFsK2wqh6AcKUVcKOw5DDpcOIQhFJGxYNwpVDV1HDrl5MU8KKw4EJUMKwZcOKwpPDkETDmMOzecOzw4YebGV9TMO3wodzIsOTwo98w7PCksOLw7TDtMO2w7wqwrPDt8OtcSfCt8OZw77DgMOCICQBw6HCtXgCCRDDi1ghw78hwpHChWxXdCXDlBYCwrzCg1kIVA/CjMKhwrjDiBrDucKDDsKwwoPDlEECEgYxw6AEPCE5wqTChApAYCF4JHgUw4XCm1XCksKdw47CucO8TMOyTMKuwqLCmGJRPMKMwoXCl8KrUsKrwp7Di8KVw5PCtyUVQsKIwpAFw6UEJ8OdwqfCmsOowp4pX8OXwr/Dv8OJE1PDg8KFBgVqwoYEFT/CjcKAwrp6cDPCuB/CrMKBw5vCqMO7EFPDncKbecK8ClXCom5Tw5TCgmDDjMOhwoHDrwpkP0Zrwq/CncKwe2oMURvCrMO7N8KDEVZjTSfCscKfw47CicKPcMO0w63Dt8KzwpNtBcKyw6ZzVmA7W8KQw60yWMKrwoADw6/DusKCVQxawq/ClSkSG8OYwrrCvU90w47Dq2RWw5vDg1BhczPDsMK+wpnCucOmw6nDjsOhw4k5KC9OJMOTRXQPw4dpw5gZLMKIw4XChMOwMsO2DUDDs8KLw57Dq8Kqw6kbS8KGS2UrL8OSw47CmMOmw5HCukMacS3DtsKDN0ARwpzDscOoCw=="
_value1 = "DcONwrcRw4AwDMOAw4DClcKYQ8OJwqTDvUfCsjs0f0jCmsOMwpzCm8K6w6LCusORPcK4d0prw47Ct8K3PMKdw4A+woDDtELCil0VwqXChg4ww41FwpzCpDbCnsK5IsKVDUjCi3lzGsONXwcRCQ/DuMKlwpQ3wpDCqcKbw5XDvhkmwrjColIFworDkT8tWMO4fcKINjIvwowjwpgmRsOGwr56GcO1f3bDpcOyEAMHw7HDgAAowrsXIsOLwo7CulQUw6oxNsOCwqnDrgc="
_value2 = "FcKMwrcRA0EQwoBaWm/DgnXDl39JesKlDFDDrMK4wo/CisKAQsKoLHbDmx/ChDV4acOCwro2JsKCRSYIw6QqR8KJImLDoD/CqUbDiMKMw5INwqc+wpDDvcKSKz/DkHddw44fEMOkRcK7wollVEPDgMKqwrfChMOFN8Kdw7PDjsOdw5FHQ1cpGcOzwrvCnMK5CS3DsMOVUkrCvDfDigLDkXknw6zDjkTDsynCiCYww7zDjQBmNMOPelLCqWPDvHHCmDTDvAA="
_value3 = "DcKNwrcNw4BADMOEVlLDlsKrVMOcfyTCuzrCgDjCghXDvlTCkHHCscOgwp/Cl8KxbkXDjSzCjSrDt8KDwqZWw6PClsOtDMKHEBHDt8KwUcOTwrzDlBwZwrxzw7nCtT7ChsOoTsOjSAt3GsKEw7JKFsKiwrcHYsK5aW5TTyjCoVnDocKAcsKmWlfDgypyLcKtwp7Dgz5oBcK4O8K+wpbDt8OMXH7DuCdUVHvCkVAXGyB7DsKCw5fClsOGTcKywpTDvh/Dn19Ww54P"
_value4 = "DcONwrkRADEIBMOBwpRAwrwyYUHDucKHdMOnw49UZxE7BQYZwqYpw6/DqhnCjcKdTWFPCwTDsBdoYcOTe8Kiw4vCuFIpwrM1A8KiwpU1FsOTwrh9BHzDg3LDhMONw5oDa2QvOMOIw70ewqUjesOgc1XCvWTCo8K8wrrDvMKiwpzCicOewrsUwo/CmX/DqMOnHMKlWDRrw7s8w7zDrAvCnMK3wrQgI8OPwrciwqp7woIxw60gw4dMwpnDjMO8C8Ohw442w7kUwp0P"
_value5 = "FcKOwrcBA0EMw4NWUg7CpcOSw60/wpLDnw0LFAAlw5rCsx9IIwEfwq8BwoDDj8Kga8Oow57CuzxOwpElwqbCg8Kaw5Uwwr/Dlx7Do8KDUATDisOKw586XA/CkTPCjnHDoWJdUsOVC8OTWxrDmsOMZUogWwzCkw0NwrTDuER+aWQRBGlew5A4wrzDtcO4wolewrwgUSlyw5LCqzZiBMKxEcOJw4gcwqzDly3DjcKLK8OGw7vCvn/CvMOzD8Oow5nDh8KFW1B/"
_value6 = "FcKPw4sRRDEIw4NaInwMHMKBwpDDvkvDmsK3V8KNRxrDq8K1bjVIw7rDrsOsw4Rdwptrw5RIIHpTw5w9w7ARSMK9QzxEKcOgLMOtCMKbNmDCtTHDp8OdChY/wrvCucKuMjMfOcO5N8KqwrPDnMKxN0Fpw7TCjMKfaivDt8OqSMK+w4k4BwvDj8O9ZhrCp8K+VsOcG8OUecOBwrxVw4tkwo4cwo9HYMKNecKkVcKZODfDgsOHWXvDuXvDsXnCs8KSw5pKKsKiwqHDuAE1"
_error_value7 = "DcONwrkRADEIBMOBwpRAwrwyYaInwMHMKBwpDDvkvDmsK3V8KNRxrDq8K1bjVIw7rDrsOsw4Rdwptrw5RIIHpTw5w9w7ARSMK9QzxEKcOgLMOtCMKbNmDCtTHDp8OdChY/wrvCucKuMjMfOcO5N8KqwrPDnMKxN0Fpw7TCjMKfaivDt8OqSMK+w4k4BwvDj8O9ZhrCp8K+VsOcG8OUecOBwrxVw4tkwo4cwo9Cs8KSw5pKKsKiwqHDuAE3"
_error_value8 = "FcKPw4sRRDEIw4NaInwMHMKBwpDDvkvDmsK3V8KNRxrDq8K1bjVIw7rDrsOsw4Rdwptrw5RIIHpTw5w9w7ARSMK9QzxEKcOgLMOtCMKbNmDCtTHDp8OdChY/wrvCucKuMjMfOcO5N8KqwrPDnMKxN0Fpw7TCjMKfaivDt8OqSMK+w4k4BwvDj8O9ZhrCp8K+VsOcG8OUecOBwrxVw4tkwo4cwo9Cs8KSw5pKKsKiwqHDuAE3"

_context = execjs.compile(doc_id_js)


@log_cost_time(describe="解密文档")
def decrypt_id(run_eval, _id):
    """
    解密doc_id
    """
    js = _context.call("GetJs", run_eval)
    js_objs = js.split(";;")
    js1 = js_objs[0] + ';'
    js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]
    key = _context.call("EvalKey", js1, js2)
    key = re.findall(r"\"([0-9a-z]{32})\"", key)[0]
    doc_id = _context.call("DecryptDocID", key, _id)
    return doc_id


@log_cost_time(describe="解密文档")
def decrypt_id_array(run_eval, _ids: list) -> dict:
    """
    解密doc_id
    """
    ret = {}
    js = _context.call("GetJs", run_eval)
    js_objs = js.split(";;")
    js1 = js_objs[0] + ';'
    js2 = re.findall(r"_\[_\]\[_\]\((.*?)\)\(\);", js_objs[1])[0]
    key = _context.call("EvalKey", js1, js2)
    key = re.findall(r"\"([0-9a-z]{32})\"", key)[0]
    doc_id_array = _context.call("DecryptDocIDArray", key, _ids)
    for i, doc_id in enumerate(_ids):
        ret[doc_id] = doc_id_array[i]
    return ret


# _test_ = "w61bS27CgzAQPQtRFkZUwr0Aw4oqR8Oow5JCUUXDksKGRUPDpcOQVcKUwrsXaEIBG8OzM8OYwoYnwqEXw6HDj3zDnsKMPTZSwrbDp8OoeMK6woYsw7pOdm8Jwosuwp/Crx8sw77DmsKfw5/DmT4+wp7CiMOneDQAGA0vIAHCsMKODFnCgiMrWcKuw5jClRBbAHgHwrMARA/CjCHCuMOgE8OEw4BhACIAWGleIMOfw4EJYgYAIMKnQD7DqAAgwp0AAMKkGAICwp7DoBxcAiARw6ANwrwGIMOPAMKAwqHDoMO6w75hwrcJw6PDizVhP2ESwrPCjX/CoMKHIH0Iw7Fuw7dsWMOxw5zDri7DvcKbSVMIAsKPOHnCh0vCqzLCs8KOw7bCnsO8dcO7w7/CvwJKwrLDpnQEdcKyHhrDkMO0wqfCpsKwOsOceUxoVlbCs1s4VmpTWcKawrjCvVDClVvDjVPDhMKZIMO0QSLCuzDCshvCo8Klw5dWwrM7wo7DqDPCrMO3w5hhE0bDjBo7VcOJfHVCwqrDqcOBwq/DlMO8IcK1RcKvTsKzSjZKa0XClsOfw73DkltTRMKmwpU5wq3DoBnCpMOPwqXDgsKqCMOMw4XCh0DDmcKzw7bDtsOcRVpLb8KlworDj1QWw4bCsSIvw5hGGsKtU8KtdsOdw4/CsAnDjnXDk27Cj8O1RBHCnVE1UMKhw4R3M8K8aDfDhSA7FcObY3ZpwrHCucOww6k0woo/wr52wrp7w5pAwobDoMOmw4nDuUpFZ8KCWmtZIB1xdzbCl0vCmDd0w400Z8KcJBcXw7XCmUnDpxlPwrJ1PRrCun8wHMOrw45yC8KQw4ZLwqBWwr/DuXTCkyxQw5Fpwr95fVpZIGzCsMORBgrCi8OswqDDk302wpzClcKWwrXDrlXDk1rCu8OcwpvCpDU2wprCvsOZwrnDhMO1fwE="
# _value_ = "FcOLwrcRBEEIAMOBwpTDkMOCwoQFw7IPw6nDr8KdwqlqY3TCm2/CnDRwwoQDF8OGwpoJwrzCslUCTMOpDhTDmicHDH1kw5HDisK3w5XChMKiwq/DqGo5w5pRGQlhVsKdXMOyah58wqFdQm7CnsK2w5ZOe2Q5wpYyL8OAQWPCqsKkwqvCiDNjwo/CjR3CuMOWUyPCk8K/WV5kT3UfLMOzRsOawp9pw6vCm8KewqHDr0k/IWwTwr1CSMKEwoMLwppYO8OMHw=="


_test = "w61aS27CgzAQPQtRFsK2wqh6AcKUVcKOw5DDpcOIQhFJGxYNwpVDV1HDrl7CoMKUEGw+KcOGwrHDoEloEMO2w7zDnsOzwozCkRHDq2PCvD/CnCMZf8KlwpvCt1TDhsKnwo/Dl3fCmXxuwo87wrlNw7YHw6Z7PgkIwqfDhQtIwoBYRsKFw4wBw4hCw5oVwrsSw5YWAsK8woNZCMKsHhjDg8OiAj/DqAA7QA3DqCABwoDDgQTCiAEnw6AJw6AACSsAwoFCcFDDsCAIN8KrKDnCnVPDuR3CpcKJXAUhwoUiwrsYw7Mvw5dcwq3Cui5XTsK/wpbClAkhfMOmFRPCnMOufcOmE8O9M8OFw6PDusO2dwLCsXw4w5MgL8KfIUHDmcKtEcOwXsOdKw3DmsKDNcOyw5bDqnbDplTDt8KmH8KvQhVZwqsUKSloMXTDuMKuwpIcw4Zow63CsTfDrcKBGsKPwqg9wqzDuz/CgxFWY03DlcOaMsOmw5XCnBPDg8KeTMKiw5MTw5fDlj9GEUzDgcKKBcOHfxTCtcOuc8KOFsKMVcOvwr0kWcKpMAsYKzgTw60/wp3DpFLDr3tyIsK4wpPDtcOswoRlw6HDmMOrw6BpwqVqwqHDrS3DlsOiAsKWw5Y+wp/DvWHCn8KUwpPDvcOYw7PDqMKXWXbCvWsJwpRZwrDDhsKJb8OQecOWScK+NMOHVwUcwpXCnyPDqMO2eUAZwq07wqQRB3DCh8OIQz7CtcKwwpzDscOgBw=="
_value1 = "DcOLwrcBw4AwDMOEw4DClShGfSnCpsO9R8KyOxQHwq7CjllRNMK0wrA6wrlpwoVowqbDm8O3wozCtDrDgMOFw5vCqMKIwr7CiSnCssKbwrs2Jlk4w7bCjsONw4HDgknDj8OmSUPDqj/Dg0Z0wq7DuRPDuMKfw7FaWVZAbcKyPybDpXDCpxsrwpXDscOcZkgfaMOcDk7DhWPDtTdOdcOIUMOnwpDDtsK2VxHCl13DtWHDtH1ePcOZEBnDpWzCgcKkWsOfKAZnwrR9"

_ids = list()
_ids.append(
    "DcOLwrcBw4AwDMOEw4DClShGfSnCpsO9R8KyOxQHwq7CjllRNMK0wrA6wrlpwoVowqbDm8O3wozCtDrDgMOFw5vCqMKIwr7CiSnCssKbwrs2Jlk4w7bCjsONw4HDgknDj8OmSUPDqj/Dg0Z0wq7DuRPDuMKfw7FaWVZAbcKyPybDpXDCpxsrwpXDscOcZkgfaMOcDk7DhWPDtTdOdcOIUMOnwpDDtsK2VxHCl13DtWHDtH1ePcOZEBnDpWzCgcKkWsOfKAZnwrR9")
_ids.append(
    "DcKOwrsVADEIw4NWwoLDsDkow4HChMO9R8K6dC4kPVMMwpN6cC5nesK3w5rDtcKWw4lIwp/ChiXDl8KUBMOJKcKbw7VyISPDuXA+w7XDhUFWPcOuecOHwo7Cu2UOw7rDlDHDn8KMwp47wqHCt8K1w6LDgnvDu3vCo8OXG8KFQFfCpkzCrMKdMA/ChD/DlS/Cn0nCrwPDngoTasKCDj3CrsOJTDRYwpcDKmXCoSPCl0tfwpEbwrgAwoHCgsO2Zi7DqMOdworDrwPDsAM=")


print(decrypt_id_array(_test, _ids))

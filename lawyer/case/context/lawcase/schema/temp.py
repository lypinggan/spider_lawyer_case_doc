# coding=utf-8
import json
from util import decrypt_id_array

json_text = """[{\"RunEval\":\"w61aw43CjsKCMBB+FsKMwoc2wph9AcOiw4lHw5jDo8KkIRvDlMKVw4PCisKpeDLCvsO7AsKLWMKgKC4Fwot8CRlCOz/Dn3xTOjRhwr4Lw5fCm2Mgw4NDwrzDvMKMZcK4w7/DvsOYw4rDqGfCtcO7wpLCq2jCvWHCrsOjwpLCgMKwWixAAsOENFbDiDskMsKRw5cVwrsSagsBw57DgSwEwqoHw4ZQXGQNYsKQMMOyBwlIHXTCgBPCsAMmw4ATwpJDSsKoAAQWwoLChcKCe8Kewr/CnAXDkcO+GMOLUxBHcsOmw7nDpMKLw6Riw4w9X1LCtcOiOl84w71ZUiLChHDCmcKTTXAqw7tMJx7Dj2TCj8Ozw5vDnwnDhMOSw6FEwoPCnHTChgQlwrdKw4DCssK6wpMbNAfCq8Ogw5bDqsOew4XCpHrDk8KPF8KhMsOUdcKKahDCtDnDnMOxXcKAbMOHwqjDssO4EHZLwo1nw5TCnsOWw73Cn0EHwqvCrsKmRsOsw405McOswqkPd8O9QFTDnsKsXsKBw7fDq8OYw7hCw4hpwrluwp/Dti/CtkFDDMK8bMKGZ8OuwpplwqUJNMK2wqfDhsOeOQzDksORVsK7PcOFwqMkclTCu8OFwosiw5rDjcKRFV84wobDg8K+CMKTw53DlcKewpTCuxECw4hRw5TDmkXCm0PCp8KVfGnDjsKYw7VeWMO6CMOVwo/Cqg7CqcODKcOZIsOywoBHCcOLGcO3fgE=\",\"Count\":\"56\"},{\"裁判要旨段原文\":\"本院经审查认为，申请人东莞市大朗伟越毛行的申请符合法律的规定。依照《中华人民共和国民事诉讼法》第一百条、第一百零二条、第一百零三条第一款的规定，裁定如下\",\"不公开理由\":\"\",\"案件类型\":\"2\",\"裁判日期\":\"2017-12-07\",\"案件名称\":\"东莞市大朗伟越毛行、东莞市汇迈服装有限公司买卖合同纠纷一审民事裁定书\",\"文书ID\":\"DcKMw4cNw4BADMKAVjp3w7vDqcK6w79ICRI/w4TDm8KewoY2wqdrND/CnsKxeMOVEVMidzfCvBLDhg3ClX8BKlRxwoDCrcOgfMK8AxHDkcKhw4sJwqlkwqMKJ1zDvlrDqsKYw7Z/FBjDh0NDFcOXwq5qP8KNw61nJMK6wr3CvMKUwrbCuMKKdsOlQj/Cu8OveR/DksOpwo3CucOHSjbCj8KJwpNzZsKbeVl4w4PDr8K5wo8kwrwURMKZWmLDoCoVw4NGwrQP\",\"审判程序\":\"一审\",\"案号\":\"（2017）粤1972民初14052号\",\"法院名称\":\"东莞市第二人民法院\"},{\"裁判要旨段原文\":\"本院认为，原告的申请符合法律规定，应予准许。依照《中华人民共和国民事诉讼法》第一百四十五条第一款、第一百五十四条第一款第（五）项的规定，裁定如下\",\"不公开理由\":\"\",\"案件类型\":\"2\",\"裁判日期\":\"2018-04-04\",\"案件名称\":\"东莞市钇伸自动化机械设备有限公司与青岛创得电子有限公司买卖合同纠纷一审民事裁定书\",\"文书ID\":\"DcOOwrcBw4AwCADCsMKXwqgGRsOqw78nJcKzFhXDpMKVQMOBbVrCvBAiw4XCosKSPcOfZ8OPaFVUwozDg8Opw4TDn8KuwqfCo2omw7ZxwpIOwrlNw5vCvHXCgR9Qw4J0w5nCmsKjw5UaFl5mAENDWcKEwrXDhRzDkMK8wpg6IcOAElTCjMKibcKJw45LGRnDl8K+dChEZlE+wq3DlMOEwoPCmxHDu8ODDUHCm2zDisONwqoBAkvDrcK6w4DDscKPwp3Cp8OeAMO2P8O4AA==\",\"审判程序\":\"一审\",\"案号\":\"（2017）粤1972民初12508号之二\",\"法院名称\":\"东莞市第二人民法院\"},{\"裁判要旨段原文\":\"本院认为，本案争议焦点在于：一、被告金泽公司应向原告支付货款本息数额是多少；二、被告朱光进是否需要对案涉债务承担连带清偿责任。&#xA;关于争议焦点一。被告金泽公司确认欠原告货款48715.4元，对于原告要求被告金泽公司支付货款48715.4元，本院予以支持。\",\"不公开理由\":\"\",\"案件类型\":\"2\",\"裁判日期\":\"2017-09-13\",\"案件名称\":\"东莞市万江文德海绵加工厂与东莞市金泽箱包有限公司、朱光进买卖合同纠纷一审民事判决书\",\"文书ID\":\"FcOLwrcBA0EIAMKwwpXDiMKhJBzDu8KPw7R2L8Ohw7N0Om3Dh8K5A1jDmcOpMMOXCDbCp8OdZxw7VsOTTsOKHSFgIsKif8OzGsKNwrzDlMOCBnzClmISwojClMOAw44SRMKuccOQwoxkwqvCqcOQX8K2w7XCjSHCtC/Dr1PCrmzClcOJTcOhK8KFX8Kfw5nCpcKOLMKrwo7DkyrDgGfDi8Kcwr11wpzCgFVObsOBw5tWwroRw4PCjMOLw6/DnsKrTHLCmMOrwrk0wp7CrMOeDw==\",\"审判程序\":\"一审\",\"案号\":\"（2017）粤1971民初3465号\",\"法院名称\":\"东莞市第一人民法院\"},{\"裁判要旨段原文\":\"本院认为，本案争议焦点在于：一、被告金泽公司应向原告支付货款本息数额是多少；二、被告朱光进是否需要对案涉债务承担连带清偿责任。&#xA;关于争议焦点一。被告金泽公司最后收货的时间是2016年11月，付款时间是月结60天，因此被告金泽公司应在2017年2月1日前\",\"不公开理由\":\"\",\"案件类型\":\"2\",\"裁判日期\":\"2017-09-13\",\"案件名称\":\"东莞市创杰织带有限公司与东莞市金泽箱包有限公司、朱光进买卖合同纠纷一审民事判决书\",\"文书ID\":\"DcKOw4sJAEEMQlvDin/DjDHDiWzDui9pB0TDoSFowqTDusOofk/CpcOdw70iRMKSwqfCj1V/RXYPwqXDk8KtZ8OiNMOOXTtdecOKQkPCgsO4wps5wqzDoC8TcsKowrnDicKiIgMPEMOmw5M6wqJaw6QzesOtTRBkw6/CrGd+N8OEwpEwwovClsKLwrvDt8Kiw7HDilDCgcOmYnwHPC7CvkzDrMOrw5JTwovCsMKkwrHCr1ZABMKSw7czwpVvwqfDhAHDhmBEZ8OKfw==\",\"审判程序\":\"一审\",\"案号\":\"（2017）粤1971民初3468号\",\"法院名称\":\"东莞市第一人民法院\"},{\"裁判要旨段原文\":\"本院认为，本案争议焦点在于：一、被告金泽公司应向原告支付货款本息数额是多少；二、被告朱光进是否需要对案涉债务承担连带清偿责任。&#xA;关于争议焦点一。被告金泽公司确认欠原告货款6782元，对于原告要求被告金泽公司支付货款6782元，本院予以支持。对于原告要求\",\"不公开理由\":\"\",\"案件类型\":\"2\",\"裁判日期\":\"2017-09-13\",\"案件名称\":\"东莞市协盛箱包辅料有限公司与东莞市金泽箱包有限公司、朱光进买卖合同纠纷一审民事判决书\",\"文书ID\":\"DcOMwrcBw4BACMOAw4DClcOgw4klccO/wpFsdWoOwrFew4MswoTDncKcw4XDrsO9TQTCvcOyw5vDt8Owwp4aAsOzWMOzTmjCmsOXG8ONJC8nOMKSw7RoPcK6ZMO0HzAXWhkLJAXDixnDnsKmw6AcwqjDg0fDncKcw75qJsKmw5E0wrd3HwNsZEZfwoUIUMKJITJMwpzDgcO8w4bCv21qwoUKwpRxAyPCqiQyAMK5JEvCkD/DgcOsElE/wokISDXCtB8=\",\"审判程序\":\"一审\",\"案号\":\"（2017）粤1971民初4359号\",\"法院名称\":\"东莞市第一人民法院\"},{\"裁判要旨段原文\":\"依照《中华人民共和国民事诉讼法》第一百六十三条的规定，裁定如下\",\"不公开理由\":\"\",\"案件类型\":\"2\",\"裁判日期\":\"2018-04-03\",\"案件名称\":\"东莞市大朗伟越毛行与曾宪兵买卖合同纠纷一审民事裁定书\",\"文书ID\":\"DcONwrkBADEIw4TDgMKWYMONw6cQMMO0X8OSXcKqYMKUfMKrYcODwrLCp8KvwpPCjMOyOU0sZMO6wojCqXLCgXHDpcKtXSkKasOXwpPCpybCjcOeGxvCq8Ohwoc/PsKkwo9oQR1Owo8owq/DtFrCuHo7FcKXByLDqsKWw6dbZkM3w7hqFEoBw47Cg8OBwrXDojjCughzI8KTAVtYwoo9w6HDtMO/wq7CqcOCw5QRwplWw4YwPhBBw7jCo8OIXsO5WR7CpcK7UCnDmAc=\",\"审判程序\":\"一审\",\"案号\":\"（2018）粤1972民初1791号\",\"法院名称\":\"东莞市第二人民法院\"}]"""

with open("./list_json.txt","r",encoding="utf-8") as fp:
    for line in fp.readlines():
        json_text = line.strip()[1:-1]
        json_text_ret = json_text.replace('\\"', '\"')
        page_data = json.loads(json_text_ret)  # 转移字符
        ids = []
        for data in page_data:
            if data.get("RunEval"):
                RunEval = data.get("RunEval")
                print("=====RunEval======")
                # print(RunEval)
                print("==================")
            elif data.get("文书ID"):
                __data = data.get("文书ID");
                # print(__data)
                ids.append(__data)

        ret = decrypt_id_array(RunEval, ids)
        print("********************")
        for _id in ret.values():
            print(_id)

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
from lawcase.js import wen_shu_js
# with open('encrypt.js', 'r') as f:
#     js = f.read()

cookies = "R3uEQTAZSdUwQ5dRfriAgJgP025LVyi5WRKUC721klSKyVuep2pl7vLT1zwyOOYDnAfEs1wxyF7v4F8nqGV0y9.u2tU3qWKj91OzRzuuZijgJc5N6nrAqwEneGDMSVtNWKvLCmO3gDxoOYzc1XVLVMYqz2OxRHQVs7esdGF3A7Vp8JhYbTDSUFRkRqIbA"  # 传入FSSBBIl1UgzbN7N80T
ctx = execjs.compile(wen_shu_js)
r = ctx.call("makemmwded", cookies, '/List/ListContent')
print(r)

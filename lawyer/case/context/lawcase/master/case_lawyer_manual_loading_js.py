# coding=utf-8
from lawyer.case.doc.doc_formatter import DocContextJsParser, Result
from lawyer.case.context.lawcase.service.pipeline import SyncCaseLawyerDocPipeline

f = open("anli", "r", encoding="utf-8")
java_script = f.read()

lawyer_id = "8af40d176783533401678782dd3002e1"
scripts = java_script.split("$(function(){$(")
for script in scripts:
    print("===========")
    ret = DocContextJsParser.parse_convert_html(script);
    print(ret)
    if ret.result:
        SyncCaseLawyerDocPipeline.sync(lawyer_id, ret.doc_id, ret.html, ret.master_domain, ret.casenum, ret.title,
                                       ret.court)


"MmEwMD=33cVkyqhbJqGLWwifTR4i.cFXBH0ARSX2_wyMf6GqdJr0SUB5tKYTW4w4BVJZO3B7DNwHTbTQc80veA7Hae8YbWrp6LcHN9E1Hahopk0ud4uAeD6dhdrajVXAM8BjgvDYMje5loLhlRBHxqQGElpSemxhmrknb.ZeVBcb0oltCkrINirUsgu3qKgQMvLJ6r_e0qNcJHkGw6hjAf6eFVcQH3jYbu06iGDX0NVOSaQ9xt6db2gsLBpHVUBYf2IiumU7yWIGdbrQhEjvQLB14N0NcUE2A77RHfWUQkv7vo0Ta06c_qA7Zh.CAghfJOlqr__rrVJxDoltzAy1yVKaYGAlosa.6XzrBcGwtukZXeTmGcfh_E"



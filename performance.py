#构造性能测试基类
import re
import time
import requests
import threading

class Performance(threading.Thread):
    #测试的时候需要根据接口method、数据类型修改__init__参数的默认值。
    def __init__(self,url="",method="post",header={},body="",body_type="json"):
        #threading.Thread.__init__(self)
        super().__init__()
        self.url = url
        self.method = method
        self.header = header
        self.body = body
        self.body_type = body_type
    #构造请求函数
    def send_request(self):
        if re.search(self.method,'get',re.I):
            #get请求参数请求参数直接跟在url后面
            r =  requests.get(self.url,headers=self.header,timeout=30)
        else:
            if self.body_type == "json":  #post到json域
                r = requests.post(self.url,headers=self.header,json = self.body,timeout=300)
            elif self.body_type == "file":#post到file域
                r = requests.post(self.url,headers=self.header,files = self.body,timeout=30)
            elif self.body == "data":     #自动放在form表单下
                r = requests.post(self.url,headers=self.header,data = self.body,timeout=30)
        return r
    #构造接口请求状态、时间函数
    def test_performance(self):
        start_time = time.time()
        try:
            #运行请求函数
            r1 = self.send_request()
            r = r1.json()
            #判断http状态码
            if r['state']['code'] == 0:
                status = "success"
            else:
                status = "fail"
        except Exception as e:
            print(e)
            status = "except"
        end_time = time.time()
        spend_time = end_time - start_time
        return (status,spend_time,r)
    #构造运行函数
    def run(self):
        self.test_performance()
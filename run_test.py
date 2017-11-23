import sys
# sys.path.append("./interface_test_")
from common import setUp_,md5
from performance import Performance

#取数组的百分比，如90%响应时间
#90%响应时间获取规则，参考lr ====平均事物响应时间
#1.Sort the transaction instances by their value.
#2.Remove the top 10% instance.
#3.The highest value left is the 90th percentile.
def get_percent_time(data_list,percent):
    #sort()方法使列表元素从小到大排序
    data_list = sorted(data_list)
    if len(data_list)*(1-percent)<= 1:
        r_length = 1
    else:
        r_length = len(data_list)*(1-percent)
        #round()方法返回浮点数x的四舍五入值。
        r_length = int(round(r_length))
    data_list = data_list[:len(data_list)-r_length]
    return data_list[-1] #返回剩下百分比中最大值被其他函数调用
#设置并发数
thread_count = 1000
#所有线程花费的时间列表
spend_time_list = []
#最大响应时间
max_time = 0
#最小响应时间
min_time = 3600
#小于0.1秒的请求数
less_than_100ms_total = 0
#大于3秒的请求数
more_than_100ms_total = 0
#成功的请求数
success_total = 0
#失败的请求数
fail_total = 0
#异常请求数
except_total = 0
#总请求数
total = 0
#请求地址，需要压力测试的接口api
# url = setUp_()[-1] + "/h5/speak/add"
# 获取话题列表
# url = setUp_()[-1] + "/h5/comment/add"
# 获取评论列表
url = setUp_()[-1] + "/h5/comment/getComment"
#构造请求头
ts = setUp_()[0]
reqId = setUp_()[1]
secret = setUp_()[2]
header = setUp_()[3]
# db = setUp_()[4]
userId = setUp_()[4]
liveId = setUp_()[5]
reqSign = reqId + ':' + secret + ':' + ts
sign = md5(reqSign)
# data = {
#     "id": reqId,
#     "timestamp": ts,
#     "sign": sign,
#     "data": {
#         "topicId": "290000451050003",
#         "type": "text",
#         "liveId": liveId,
#         "content": "我正在发言,后面是小尾巴是不是很神奇..." + ts,
#         "isReplay": "N",
#         "page": {"size": "20", "page": "1"},
#         "userId": userId
#     }
# }
# 增加评论的
# data = {
#     "id": reqId,
#     "timestamp": ts,
#     "sign": sign,
#     "data": {
#         "topicId": "290000451050003",
#         "liveId": liveId,
#         "isQuestion":"Y",
#         "content":"我正在发言,后面是小尾巴是不是很神奇..." + ts,
#         "type":"text",
#         "page": {"size": "20", "page": "1"},
#         "userId": userId
#     }
# }
data = {
    "id": reqId,
    "timestamp": ts,
    "sign": sign,
    "data": {
        "topicId": "290000451050003",
        "liveId": liveId,
        "time":ts,
        "beforeOrAfter":"before",
        "page": {"size": "20", "page": "1"},
        # "userId": userId
    }
}
#初始化测试次数i、所有线程总花费时间
i = 0
time_total = 0
#构造线程组测试接口
while i < thread_count:
    #实例化类,传入url、请求头、请求方法、post方法要传输参数body
    pf = Performance(url=url,header=header,body=data,)
    status = pf.test_performance()[0]
    spend_time = pf.test_performance()[1]
    print(pf.test_performance()[2])
    print(i)

    #respond = pf.send_request()
    spend_time_list.append(spend_time)
    total = total + 1
    if status == "success":
        success_total +=1
    elif status == "fail":
        fail_total += 1
    elif status == "except":
        except_total += 1
    if spend_time > max_time:
        max_time = spend_time
    if spend_time < min_time:
        min_time = spend_time
    if spend_time > 0.1:
        more_than_100ms_total += 1
    else:
        less_than_100ms_total += 1
    time_total += spend_time
    pf.start() #运行线程组
    i += 1

#平均响应时间
avg_time = time_total/thread_count
# 吞吐率 = 并发用户数下单位时间内处理的请求数
RPS = thread_count/time_total

#响应时间列表从小到大排序
spend_time_list = sorted(spend_time_list)
print("平均响应时间：%s"% avg_time)
print("最大响应时间：%s"% max_time)
print("最小响应时间：%s"% min_time)
print("90%%响应时间：%s"%(get_percent_time(spend_time_list,0.9)))
print("99%%响应时间：%s"% (get_percent_time(spend_time_list,0.99)))
print("80%%响应时间：%s"% (get_percent_time(spend_time_list,0.8)))
print("总请求数：%s"% total)
print("请求成功数：%s"% success_total)
print("请求失败数：%s"% fail_total)
print("异常请求数：%s"% except_total)
print("大于100毫秒请求数：%s"% more_than_100ms_total)
print("小于100毫秒请求数：%s"% less_than_100ms_total)
thread_count = str(thread_count)
RPS = str(RPS)
print("并发"+ thread_count + "个请求的吞吐率是：" + RPS)


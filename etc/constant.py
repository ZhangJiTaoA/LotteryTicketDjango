# sql常量
host = "8.146.207.26"
username = "root"
password = "597778912"
database = "LotteryTicket"
port = 3306
charset = 'utf8mb4'
engine = 'mysql+pymysql://' + username + ':' + password + '@' + host + ':' + str(
    port) + '/' + database + '?charset=utf8mb4'

"""
# 爬虫常量
"""
# 福利彩票爬虫网址
flcp_base_url = "https://www.cwl.gov.cn/"
ssq_suffix_url = "/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}
# 开奖爬虫网址，爬取历史数据
kj_base_url = "https://kaijiang.78500.cn/"
kj_ssq_url = "/ssq/"

"""
# 数据库表常量
"""
# 双色球常量
ssq_db_name = "SSQ"
ssq_columns = ['issue', 'time', 'blue', 'red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'content', 'amount']

ssq_red_start = 1
ssq_red_end = 32
ssq_blue_start = 1
ssq_blue_end = 16
ssq_red_length = 6
ssq_blue_length = 1

'''
其他常量
'''
# 时间常量
date_format = "%Y-%m-%d"
specific_format = '%Y-%m-%d %H:%M:%S'
seconds_in_day = 86400

# 用户信息
user = ["openid", "unionid", "session_key", "gender", "age", "logintime", "score"]
init_score = 50

appid = "wx4081ef0a8bde8e45"
appsecret = "4372f48297075b34b7a0676893b096ad"
# 调用微信接口，获得openid等信息
code2Session_url = "https://api.weixin.qq.com/sns/jscode2session"

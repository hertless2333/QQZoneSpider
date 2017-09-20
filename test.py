import requests
import json
import threading
from random import choice

class Craw(threading.Thread):
    def __init__(self, start, end):
        threading.Thread.__init__(self)
        self.try_count = 0    #用来测试的计数变量
        self.info_list = []
        self.url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=1248703394&hostUin=1002998443&start={}&s=0.08334211819767567&format=jsonp&num=10&inCharset=utf-8&outCharset=utf-8&g_tk=724411949&qzonetoken=d04e2bd6d8f4b65c69df6152e24ba64ce1cd68eb11533222010403a651527f921ac06056b064668f2267&g_tk=724411949'
        self.start_num = start
        self.end_num = end
        self.headers = {
              'accept': "*/*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.8",
    'cookie': "pgv_pvi=9705235456; pgv_pvid=6345624258; RK=C81Kyl4/ZP; __Q_w_s__QZN_TodoMsgCnt=1; __Q_w_s_hat_seed=1; zzpaneluin=; zzpanelkey=; pgv_si=s758123520; _qpsvr_localtk=0.7302239509348496; ptisp=cnc; ptcz=a82ea318cc83889d3fb5f9011b10326638813005d79e7963752513a9507c927f; pt2gguin=o1248703394; uin=o1248703394; skey=@t2Hmw05IY; p_uin=o1248703394; p_skey=bIEIismZ481JCR7nwAyicrtBI-dcs6BmgwRVxkiZDkw_; pt4_token=Kn5Z6I9ovKkppW3wR1D0WIVisjDMQ9foCknhEMkLYgc_; pgv_info=ssid=s8031021202; rv2=80644E04A1265FEA3F7FDD4007F8857D0FAE39139F5DEA8A7E; property20=0E4CDFFC74DBF531493825D90208D8495A0E964B1F8EC3621B4788D664FAC45E59BEF135635C8D3B",
    'referer': "https://user.qzone.qq.com/1002998443/334?_t_=0.20855940877625256",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    'cache-control': "no-cache",
    'postman-token': "1a22e0e8-707d-ad0d-61dc-90ef7f69a4f1"
        }
        self.agent = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'
        ]
        self.querystring = {"_t_":"0.20855940877625256"}

    def get_info(self):
        url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=1248703394&hostUin=1002998443&num=10&start=170&hostword=0&essence=1&r=0.7012575261977094&iNotice=0&inCharset=utf-8&outCharset=utf-8&format=jsonp&ref=qzone&g_tk=724411949&qzonetoken=d04e2bd6d8f4b65c69df6152e24ba64ce1cd68eb11533222010403a651527f921ac06056b064668f2267&g_tk=724411949'
        html = ''
        while html == '':
            try:
                self.headers['user-agent'] = choice(self.agent)
                response = requests.request("GET", url, headers=self.headers, params=self.querystring)
                html = response.text[10:-3]
                print(html)
            except Exception as e:
                print(e)
                print("休息三秒\n" + url)
                html = ''
        # for comment in js['data']['commentList']:
        #     print(comment['nickname'] + str(self.try_count))
        #     self.try_count += 1


craw = Craw(0, 500)
craw.get_info()
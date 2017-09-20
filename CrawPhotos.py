#爬取qq空间某相册下的所有图片
#使用多线程爬取的信息
#cookies需要更改
#图片不上传了

import requests
import json
from random import choice
import threading
from time import time

class Craw(threading.Thread):
    def __init__(self, start_pic, num_pic):
        threading.Thread.__init__(self)
        self.start_pic = start_pic
        self.num_pic = num_pic
        self.agent = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'
        ]
        self.url = "https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?g_tk=1799128936&callback=shine0_Callback&t=541721287&mode=0&idcNum=4&hostUin=1002998443&topicId=V13tL5ZX1SBtjX&noTopic=0&uin=1248703394&pageStart={}&pageNum={}&skipCmtCount=0&singleurl=1&batchId=&notice=0&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&outstyle=json&format=jsonp&json_esc=1&question=&answer=".format(self.start_pic, self.num_pic)
        self.headers = {
            'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8",
            'cookie': "pgv_pvi=9705235456; pgv_pvid=6345624258; RK=C81Kyl4/ZP; __Q_w_s__QZN_TodoMsgCnt=1; zzpaneluin=; zzpanelkey=; pgv_si=s9083886592; _qpsvr_localtk=0.31353370108415923; ptisp=cnc; ptcz=a82ea318cc83889d3fb5f9011b10326638813005d79e7963752513a9507c927f; pt2gguin=o1248703394; uin=o1248703394; skey=@KRkss4GvC; p_uin=o1248703394; p_skey=BylvlMw7wkwHFDTf7q7WVbBJT5fcBMPZ2ROTwAk89BY_; pt4_token=j*PmqpLN6fmaySLahg0SAimU2gyP4UJNr4qzjhDNGtU_; pgv_info=ssid=s4282978570; qq_photo_key=aa6d26fc879f268309518d27d0a90127; rv2=807D2D1FA33A36FB6CA7E8691B0A33A00C9E85D13D1D8C8728; property20=6B54F17283E8F9A50A004A6889CEAFC0427DC10F7A2875C228ECAD69CEE10F7BA615E2E4F77C2511",
            'referer': "https://qzs.qq.com/qzone/photo/v7/page/photo.html?init=photo.v7/module/photoList2/index&navBar=1&normal=1&aid=V13tL5ZX1SBtjX",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            'cache-control': "no-cache",
            'postman-token': "47520b4d-a12d-9acd-21cc-bfcaf5a57225"
        }
        self.querystring = {"_t_":"0.6402952631079735"}
        self.pic_list = []
        self.count = 0

    def run(self):
        html = ''
        while html == '':
            try:
                self.headers['user-agent'] = choice(self.agent)
                response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
                html = response.text.split('(')[1]
                html = html.split(')')[-2]
                js = json.loads(html)
            except Exception as e:
                print(e)
                print("休息三秒")
        for i in range(self.num_pic):
            pic_url = js['data']['photoList'][i]['url']
            self.pic_list.append(pic_url)
            self.count += 1
        print('正在爬取图片url：共有{}张,已经完成{}张'.format(self.num_pic, self.count))

class Download(threading.Thread):
    def __init__(self, list, num):
        threading.Thread.__init__(self)
        self.url_list = list
        self.path = 'pic/{}.jpg'
        self.album = num
        self.count = 0

    def run(self):
        count = (self.album - 1) * 500
        for url in self.url_list:
            path = self.path.format(count)
            r = requests.get(url)
            with open(path, 'wb') as f:
                f.write(r.content)
                count += 1
                self.count += 1
        print('线程{}下载完成'.format(self.album))


if __name__ == "__main__":
    start_time = time()
    print('正在爬取wuliwuwu的相册。。。')
    craw1 = Craw(0, 500)
    craw1.start()
    craw2 = Craw(500, 500)
    craw2.start()
    craw3 = Craw(1000, 475)
    craw3.start()
    craw1.join()
    craw2.join()
    craw3.join()
    print('\n爬取完成，准备下载。。')
    d1 = Download(craw1.pic_list, 1)
    d1.start()
    d2 = Download(craw2.pic_list, 2)
    d2.start()
    d3 = Download(craw3.pic_list, 3)
    d3.start()
    d1.join()
    d2.join()
    d3.join()
    end_time = time()
    print('任务完成，共用时{}秒'.format(end_time-start_time))



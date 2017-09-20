#爬取某个好友所有留言的爬虫
#多线程
#修改cookie

import requests
import json
import threading
from random import choice

class Craw(threading.Thread):
    def __init__(self, start, end):
        threading.Thread.__init__(self)
        self.try_count = start    #用来测试的计数变量
        self.info_list = []
        self.url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb?uin=1248703394&hostUin=1002998443&start={}&s=0.03812245807939996&format=jsonp&num=10&inCharset=utf-8&outCharset=utf-8&g_tk=1372700294&qzonetoken=57e3a7f14c209a9072fa74aae504946e8791d2c4de1f9948bbf0b4680a4e1ef59929edd4987b6506bdc0&g_tk=1372700294'
        self.start_num = start
        self.end_num = end
        self.headers = {
             'accept': "*/*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.8",
    'cookie': "pgv_pvi=9705235456; RK=C81Kyl4/ZP; __Q_w_s__QZN_TodoMsgCnt=1; __Q_w_s_hat_seed=1; pgv_pvid=6345624258; zzpaneluin=; zzpanelkey=; pgv_si=s9473046528; _qpsvr_localtk=0.568789709476516; ptisp=cnc; ptcz=a82ea318cc83889d3fb5f9011b10326638813005d79e7963752513a9507c927f; pt2gguin=o1248703394; uin=o1248703394; skey=@UDYUi9CX1; p_uin=o1248703394; p_skey=xYsZgTIMeO2DYEJwz0Syl5u6I54a*SuZs15Jmk9wObM_; pt4_token=o3BTRmfZgmLoErJHhV7RAHyGywBSyR4cYQbpa5Jic-A_; pgv_info=ssid=s979396779; rv2=803E135A60D9833E31B43E266042725389DA89B31C46180DB3; property20=21287FED921B1BF1CA63076AD70921451DA1862FB6BA8BA0C4BECB1E5679DEA306C1CDAF0EF7B122",
    'referer': "https://user.qzone.qq.com/1002998443/334",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    'cache-control': "no-cache",
    'postman-token': "4b02ad09-1deb-54af-c98d-e846767ad636"
        }
        self.agent = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'
        ]

    def get_info(self, url):
        html = ''
        while html == '':
            try:
                self.headers['user-agent'] = choice(self.agent)
                response = requests.request("GET", url, headers=self.headers)
                html = response.text[10:-3]
                js = json.loads(html)
            except Exception as e:
                print(e)
                print("休息三秒\n" + url)
                html = ''
        for comment in js['data']['commentList']:
            try:
                #self.info_list.append([comment['nickname'], comment['pubtime'], comment['ubbContent']])
                self.info_list.append(comment['ubbContent'])   #根据具体需要的信息选择
            except:
                self.info_list.append('私密留言')
            self.try_count += 1
            print('\r当前线程进度：{}/{}'.format(self.try_count - self.start_num, self.end_num - self.start_num), end='')


    def run(self):
        num  = self.start_num
        while num < self.end_num:
            url = self.url.format(num)
            self.get_info(url)
            num += 10        #留言板上开始的数目必须是10的整数倍

class Write:
    def __init__(self, list):
        self.path = 'comments.txt'
        self.info_list = list
        self.count = 0

    def run(self):
        for list1 in self.info_list:
            #如果需要具体的信息，将使用以下代码
            # for info in list1:
            #     with open(self.path, 'a', encoding='utf-8') as f:
            #         f.write(info + '\n')
            #如果只是需要写入留言，用下面的代码
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(list1)
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write('\n')
                print('\r正在写入中，写入进度{}/{}条'.format(self.count, len(self.info_list)), end='')
                self.count += 1


if __name__ == '__main__':
    craw1 = Craw(0, 1000)
    craw1.start()
    craw2 = Craw(1000, 2000)
    craw2.start()
    craw3 = Craw(2000, 3000)
    craw3.start()
    craw4 = Craw(3000, 4083)
    craw4.start()
    craw1.join()
    craw2.join()
    craw3.join()
    craw4.join()
    print('\n留言爬取完成，正在写入...\n')
    infor_list = []
    infor_list.extend(craw1.info_list)
    infor_list.extend(craw2.info_list)
    infor_list.extend(craw3.info_list)
    infor_list.extend(craw4.info_list)
    write = Write(infor_list)
    write.run()
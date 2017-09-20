#爬取某个好友所有说说的爬虫
#多线程
#修改cookie

import requests
import json
import threading
from random import choice

class Craw(threading.Thread):
    def __init__(self, start, end):
        threading.Thread.__init__(self)
        self.pos_start = start
        self.count = start
        self.emo_list = []
        self.pos_end = end
        self.url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=1002998443&ftype=0&sort=0&pos={}&num=20&replynum=100&g_tk=2147336051&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken=ed22a204f80c1fe82ff8c4723a4b0546cca012c3956f78b54177ae03a94bcb5f6d657fe7ccbd7c2b4c82&g_tk=2147336051'
        self.agent = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'
        ]
        self.headers = {
            'accept': "*/*",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8",
            'cookie': "pgv_pvi=9705235456; pgv_pvid=6345624258; RK=C81Kyl4/ZP; __Q_w_s__QZN_TodoMsgCnt=1; __Q_w_s_hat_seed=1; zzpaneluin=; zzpanelkey=; pgv_si=s621085696; _qpsvr_localtk=0.12438710564938593; ptisp=cnc; ptcz=a82ea318cc83889d3fb5f9011b10326638813005d79e7963752513a9507c927f; pt2gguin=o1248703394; uin=o1248703394; skey=@UDYUi9CX1; p_uin=o1248703394; p_skey=pNAZz1c3*hoVVs-FA7HYuE4X981SHR-btPhEOEI5XAI_; pt4_token=nSLK5UqYHOq*fOTJSEl86*8h8M-G4x8Jt3CPtebdMIE_; pgv_info=ssid=s1870942361; rv2=80D4733FE712323AA004931C7C373AAF7BF47F9E769841E4B8; property20=3094E2B94A39323E7B7EA9956860FE2F253C2E57228630812F74C3FA15115BE5747CF764EB8FC939",
            'referer': "https://user.qzone.qq.com/1002998443/main",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            'cache-control': "no-cache",
            'postman-token': "3f935b7b-78cb-31e6-1495-4f633b41a954"
        }

    def get_info(self, url):
        html = ''
        while html == '':
            try:
                self.headers['user-agent'] = choice(self.agent)
                r = requests.get(url, headers = self.headers)
                html = r.text[17:-2]
                js = json.loads(html)
                for emotion in js['msglist']:
                    self.emo_list.append([emotion['createTime'], emotion['content']])
                    print('\r本线程进度：{}/{}'.format(self.count - self.pos_start, self.pos_end - self.pos_start), end='')
                    self.count += 1
            except Exception as e:
                print(e)
        # print(self.emo_list)

    def run(self):
        count = self.pos_start
        while count < self.pos_end:
            url = self.url.format(count)
            print(url)
            self.get_info(url)
            count += 20

class Write:
    def __init__(self, list):
        self.path = 'emotions.txt'
        self.emo_list = list
        self.count = 0

    def run(self):
        for emotion in self.emo_list:
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(emotion[0] + ':\n' + emotion[1] + '\n\n')
                print('\r正在写入文件，共{}/{}条'.format(self.count, len(self.emo_list)), end='')
                self.count += 1


if __name__ == '__main__':
    craw1 = Craw(0, 200)
    craw1.start()
    craw2 = Craw(200, 420)
    craw2.start()
    craw1.join()
    craw2.join()
    info_list = []
    info_list.extend(craw1.emo_list)
    info_list.extend(craw2.emo_list)
    print('共' + str(len(craw1.emo_list)) + '+' + str(len(craw2.emo_list)) + '条')
    write = Write(info_list)
    write.run()




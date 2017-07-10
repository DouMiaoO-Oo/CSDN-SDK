# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import bs4
import urllib
import urllib.request
import urllib.parse
import json
import os

__author__ = 'DouMiaoO_Oo'
__date__ = 2017 / 7 / 2


def save_obj(obj, name):
    """
    将 obj 序列化存入本地文件
    :param obj:
    :param name:
    :return:
    """
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name ):
    """
    将序列化存储的内容从本地文件中读出来
    :param name:
    :return:
    """
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_json_to_file(json_dict):
    """
    把 json 存入文件，用缩进分隔
    :param json_dict:
    :return:
    """
    with open('csdn.html', 'w', encoding='utf-8') as file:
        # ensure_ascii 为 False
        file.write(json.dumps(json_dict, indent=4, ensure_ascii=False, separators=(',', ': ')))


class CsdnOAuthV2:
    """
    csdn 客户端版本的类，用来进行一些需要的操作
    """
    def __init__(self):
        self.access_token = self.get_csdn_access_token()

    @staticmethod
    def get_csdn_access_token():
        """
        利用客户端的方式登录，解析 response 中的json格式数据
        :return: 解析好的 json，保存为 dict
        """
        url = 'http://api.csdn.net/oauth2/access_token?client_id=%s' \
              '&client_secret=%s' \
              '&grant_type=password' \
              '&username=%s' \
              '&password=%s'

        ACCESS_KEY = os.getenv("CSDN_ACCESS_KEY")  # client_id
        SECRET_KEY = os.getenv("CSDN_SECRET_KEY")  # client_secret
        USER_NAME = os.getenv("CSDN_USER_NAME")
        PASSWORD = os.getenv("CSDN_PASSWORD")

        # print(url % (ACCESS_KEY, SECRET_KEY, USER_NAME, PASSWORD))
        response = urllib.request.urlopen(url % (ACCESS_KEY, SECRET_KEY, USER_NAME, PASSWORD))
        res = response.read().decode()
        response.close()
        return json.loads(res, encoding="utf-8")['access_token']

    def get_article_list(self, status="enabled", page=1, size=15):
        """
        api doc: http://open.csdn.net/wiki/api/blog/getarticlelist
        :param status: enabled|draft
        :param page:
        :param size:
        :return:
        """
        query_para = urllib.parse.urlencode({'access_token': self.access_token, 'status': status,
                                             'page': page, 'size':size})
        url = 'http://api.csdn.net/blog/getarticlelist?'+query_para
        response = urllib.request.urlopen(url)
        res = response.read().decode()
        response.close()
        return json.loads(res, encoding="utf-8")

    def save_article(self, title, content, type="original", **kw):
        """
        这一页的 csdn api 有错误，应该是repost 而不是 report
        api doc: http://open.csdn.net/wiki/api/blog/savearticle
        这里应该用 post 方法吧，毕竟要传输那么多博客内容
        :param title:
        :param type: original|repost|translated
        :param content:
        :param kw:
                   id, modify article need to specify id.
                   description
                   categories
                   tags
                   ip
        :return:
        """
        req = urllib.request.Request('')  # http post method
        para_dict = {'access_token': self.access_token}

        if type not in ('original', 'report', 'translated'):
            print("type 参数只有三个合法值 original | repost | translated")
            # 这里应该抛出一个异常比较好
            return None
        if kw.__contains__('id'):
            para_dict[id] = kw['id']
        if kw.__contains__('description'):
            para_dict[id] = kw['id']

    def get_article(self, article_id):
        """
        api doc: http://open.csdn.net/wiki/api/blog/getarticle
        :param article_id: article id
        :return: title
        """
        query_para = urllib.parse.urlencode({'access_token': self.access_token, 'id': article_id})
        url = 'http://api.csdn.net/blog/getarticle?' + query_para
        print(url)
        response = urllib.request.urlopen(url)
        res = response.read().decode()  # decode from bytes to utf-8
        return json.loads(res, encoding='utf8')

if __name__ == '__main__':
    csdnOAuthV2 = CsdnOAuthV2()
    article_list = csdnOAuthV2.get_article_list(page=1)
    save_json_to_file(article_list)
    # article = csdnOAuthV2.get_article('51446945')
    # article = csdnOAuthV2.get_article('52838629')  # windows python uninstall
    # article = csdnOAuthV2.get_article('51441041')  #
    article = csdnOAuthV2.get_article('51296992')  #
    with open('article2', 'w', encoding='utf8') as f:
        f.write(article["content"])

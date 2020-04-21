from aiocqhttp import *
# import sys
# sys.path.append("..")
import aiohttp
import asyncio
import botbasic
import config
import datetime
import json
import random
import time
import urllib
useddata = []
bot = CQHttp()


class jifen:
    """
    每日签到
    """
    bot = CQHttp()
    mod = {}
    data = []

    def init(self):
        pass

    async def getqqmusic(self, key):
        async with aiohttp.ClientSession() as session:
            # data.append(key)
            apiurl = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?format=json&w='
            url = apiurl + urllib.parse.quote(key.encode("utf-8"))
            resp = await session.get(url)
            ret = await resp.text()
            ret = json.loads(ret)
            f = open("music.json", "w")
            json.dump(ret, f, ensure_ascii=False, indent=4)
            f.close()
            info = ret["data"]["song"]["list"][0]
            url = "https://y.qq.com/n/yqq/song/%s.html" %(info["songmid"])
            song_name = info["songname"]
            singers = info["singer"]
            singer_name = ""
            for singer in singers:
                singer_name += singer["name"] + " / "
            singer_name = singer_name[:-3]
            img_url = "http://y.gtimg.cn/music/photo_new/T002R300x300M000%s.jpg" % (info["albummid"])
            text = botbasic.text_share(url=url, title=song_name, content=singer_name, image=img_url)
        return text
    async def getbilibili(self, id):
        print(id)
        # text = botbasic.text_share()
        # 虽然我想用 avid 但是emm...
        videourl = "https://www.bilibili.com/video/{0}".format(id)
        if id[0:2] == "av" or id[0:2] == "AV":
            id = id[2:]
            # url = https://api.bilibili.com/x/web-interface/view?aid=96128672&cid=164101749
            url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(id)
        elif id[0:2] == "BV":
            url = "https://api.bilibili.com/x/web-interface/view?bvid={0}".format(id)
        else:
            return "错误，目前支持 #B站 avxxxx #B站 BVXXXXXX 的形式"
        async with aiohttp.ClientSession() as session:
            apiurl = url
            resp = await session.get(url)
            ret = await resp.text()
            ret = json.loads(ret)
            f = open("bilibili.json", "w")
            json.dump(ret, f, ensure_ascii=False, indent=4)
            f.close()
            info = ret["data"]
            title = info["title"]
            # title = "123"
            image = info["pic"] # + "@360w_203h_1c_100q.webp"
            image = image.replace("http://", "https://")
            url = videourl
            content = "UP主: {0} 分区:{1} 简介:{2}".format(info["owner"]["name"], info["tname"], info["desc"])
            print(botbasic.text_share(url=url, title=title, content = content, image=image))
            return botbasic.text_share(url=url, title=title, content = content, image=image)

    async def reply(self, event):  # 通过 event 区分来源，一般可以直接 botbasic.reply() 返回
        msg, group_id, user_id = botbasic.getmsg_full(event)
        mm = msg.split(" ")
        msg = msg[len(mm[0]) + 1:]
        if mm[0] == "#点歌":
            key = msg
            text = await self.getqqmusic(key)
            # text = botbasic.music_share(url=url, audio="", title=song_name, content=singer_name, image=img_url)
            await botbasic.reply(event=event, text=text, at=True)
        elif mm[0] == "#bilibili" or mm[0] == "#B站" or mm[0] == "#b站":
            id = msg
            text = await self.getbilibili(id)
            await botbasic.reply(event=event, text=text, at=True)

    async def check(self, event):
        """是否向下传递"""
        msg = botbasic.getmsg(event)
        msg = msg.split(" ")
        command = ["#点歌", "#bilibili", "#B站", "#b站"]
        if msg[0] in command:
            return 2
        else:
            return 0
        return 0

    def importdata(self, _data):
        # 将本地的数据转化成程序数据
        self.data = _data
        return

    def exportdata(self):
        # 导出然后结束
        return self.data

    @classmethod
    def class_info(cls):
        return {
            "name": "点播系统",
            "sign": "com.zsh2517.pycqp.music",
            # 这个会在菜单里面显示
            "version": "1.0",
            "author": "zsh2517",
            "description": "点播系统(目前唯一一个真正有实际意义的功能😂)",
            # 上面 关于 <模块名>
            "help": """点播系统
为什么不叫点歌了呢？后面会考虑别的平台
【#点歌 歌曲名】 发送QQ音乐里面该歌曲名的第一首歌""",
            # 上面所有的东西 帮助 <模块名>
            "pluginver": 3,
            "type": "global"
        }

    def __init__(self, setbot, moduleall=None, db=None):
        "这里主要是模块自身的初始化"
        bot = setbot
        self.mod = moduleall
        self.data = {}


def this():
    return jifen

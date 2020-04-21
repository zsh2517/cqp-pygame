from aiocqhttp import *
# import sys
# sys.path.append("..")
import config
import botbasic
import json
import random

useddata = []
bot = CQHttp()


class menu:
    """
        这里是样例模板
        由于想着不同的人进行分离框架，所以这里换成了类，然后可选的每个人一个实例或者是所有人一个实例
    """
    bot = CQHttp()
    mod = {}
    def init(self):
        pass

    async def reply(self, event):  # 通过 event 区分来源，一般可以直接 botbasic.reply() 返回
        message = botbasic.getmsg(event)
        text = "\n机器人功能列表\n==================\n"
        if message == "#菜单" or message == "#menu":
            for i in range(0, len(self.mod)):
                name = self.mod[i]["module"].this().class_info()["name"]
                text += name + "\n"
        await botbasic.reply(event=event, text=text, at=True)



    async def check(self, event):
        "是否向下传递"
        message = botbasic.getmsg(event)
        if message[0:3] == "#菜单" or message[0:5] == "#menu":
            return 2
        else:
            return 0

    @classmethod
    def class_info(cls):
        return {
            "name": "菜单",
            # 这个会在菜单里面显示
            "version": "1.0",
            "author": "zsh2517",
            "sign": "com.zsh2517.pycqp.menu",
            "description": "机器人的功能菜单",
            # 上面 关于 <模块名>
            "help": """直接使用 #菜单 或者 #menu 即可
            """,
            # 上面所有的东西 帮助 <模块名>
            "pluginver": 2,
            "type": "global"
        }

    def __init__(self, setbot, moduleall=None, db=None):
        "这里主要是模块自身的初始化"
        bot = setbot
        self.mod = moduleall

def this():
    return menu
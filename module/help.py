from aiocqhttp import *
# import sys
# sys.path.append("..")
import config
import botbasic
import json
import random

useddata = []
bot = CQHttp()


class help:
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
        text = "\n"
        if message == "#帮助" or message == "#help":
            text += "使用 #帮助 [功能名称] 可以打开该功能的帮助\n"
            for i in range(0, len(self.mod)):
                name = self.mod[i]["module"].this().class_info()["name"]
                description = self.mod[i]["module"].this().class_info()["description"]
                text += name + "    " + description + "\n"
        else:
            message = message.replace("#帮助", "").replace("#复读", "").replace(" ", "")
            for i in range(0, len(self.mod)):
                name = self.mod[i]["module"].this().class_info()["name"]
                if message == name:
                    text = self.mod[i]["module"].this().class_info()["help"]
        await botbasic.reply(event=event, text=text, at=True)

    async def check(self, event):
        "是否向下传递"
        message = botbasic.getmsg(event)
        # 0 无响应（继续传递）
        # 1 有响应（继续传递）
        # ↑↑↑↑这个不会调用reply，仅仅是为了以后的扩展
        # 2 有响应（不继续传递）
        # 3 独占模式（后面的消息仅发送给当前程序）
        # 4 退出独占模式
        if message[0:3] == "#帮助" or message[0:5] == "#help":
            return 2
        else:
            return 0

    @classmethod
    def class_info(cls):
        return {
            "name": "帮助",
            # 这个会在菜单里面显示
            "version": "1.0",
            "author": "zsh2517",
            "sign": "com.zsh2517.pycqp.help",
            "description": "显示目前所有模块的帮助信息",
            # 上面 关于 <模块名>
            "help": """直接使用 #帮助 或者 #help 即可查查看帮助列表
这个会调用 name 和 description
#帮助 菜单名称
会调用对应菜单名称的 help""",
            # 上面所有的东西 帮助 <模块名>
            "pluginver": 2,
            # 模块版本，这个不会显示出来，为了实现兼容可能要用
            "type": "global"
            # 模块类别：
            # global 是 全局模块，在所有群共享一个实例（节省资源）
            # 例如 让我帮你百度一下 点歌 等等
            # group 是 群模块：在一个群共享一个实例
            # 例如 例如一些游戏模块、成语接龙 等等，全群参与的
            # user-global 是 个人模块，但是可以跨群
            # 例如备忘录提醒等等
            # 如果需要更为复杂的，例如狼人杀助手等等，请选择 global 然后自行处理共享。
            # 这个仅仅是由框架进行实例的分离。从而方便制作
            # user-single 个人模块，每个群、私聊是独立的
        }

    def __init__(self, setbot, moduleall=None, db=None):
        "这里主要是模块自身的初始化"
        bot = setbot
        self.mod = moduleall


def this():
    return help

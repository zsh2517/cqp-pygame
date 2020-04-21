from aiocqhttp import *
# import sys
# sys.path.append("..")
import config
import botbasic
import json
import random

useddata = []
bot = CQHttp()


class admin:
    """
        管理插件 
    """
    bot = CQHttp()
    mod = {}

    def init(self):
        pass

    async def reply(self, event):  # 通过 event 区分来源，一般可以直接 botbasic.reply() 返回
        message = botbasic.getmsg(event)
        text = "\n"
        if message == "#save":
            await botbasic.reply(event, "正在保存数据", at=True)
            botbasic.savedata(self.mod)
            await botbasic.reply(event, "保存完成", at=True)

    async def check(self, event):
        message, group_id, user_id = botbasic.getmsg_full(event)
        if message == "#save":
            if str(user_id) != "865564024":
                await botbasic.reply(event, "无权限使用", at=True)
                return 0
            return 2
        else:
            return 0

    @classmethod
    def class_info(cls):
        return {
            "name": "管理",
            # 这个会在菜单里面显示
            "version": "1.0",
            "author": "zsh2517",
            "sign": "com.zsh2517.pycqp.help",
            "description": "机器人管理模块",
            # 上面 关于 <模块名>
            "help": """暂无详细信息""",
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
    return admin

from aiocqhttp import *
# import sys
# sys.path.append("..")
import config
import botbasic
import json
import random
import datetime

useddata = []
bot = CQHttp()


class jifen:
    """
    每日签到
    """
    bot = CQHttp()
    mod = {}
    data = {}

    def init(self):
        pass

    async def reply(self, event):  # 通过 event 区分来源，一般可以直接 botbasic.reply() 返回
        msg, group_id, user_id = botbasic.getmsg_full(event)
        if msg == "#签到":
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            if date not in self.data.keys():
                self.data[date] = []
            flag = False
            for i in range(0, len(self.data[date])):
                if self.data[date][i]["user"] == user_id:
                    flag = True
                    break
            if flag:
                await botbasic.reply(event=event, text="你已经签过到了\n不能重复签到", at=True)
                return
            gold = random.randint(5, 15)
            self.data[date].append({
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": event.user_id,
                "earn": gold
            })
            text = "签到成功\n获得了 %d 金币\n你是今天第%d个签到的" % (gold, len(self.data[date]))
            await botbasic.reply(event=event, text=text, at=True)

    async def check(self, event):
        # """是否向下传递"""
        # msg = botbasic.getmsg(event)
        # if msg[0:3] == "#签到":
        #     return 2
        # else:
        #     return 0
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
            "name": "积分系统",
            "sign": "com.zsh2517.pycqp.jifen",
            # 这个会在菜单里面显示
            "version": "1.0",
            "author": "zsh2517",
            "description": "积分系统（未启用），包括比如金币（目前只有金币）等等一系列的数值系统",
            # 上面 关于 <模块名>
            "help": """积分系统(暂未启用)
以下的积分代指例如金币以及可能会出现的等级等等一系列的数据
【#查询我的积分】 查询自己的所有积分
【#查询积分 @某个人】 查询对方的所有积分
【#改变 @某个人 数值名称 值】 改变某个人的某个值
【#设置 @某个人 数值名称 值】 设置某个人的某个值
例如 【#改变 @张三 金币 -10】 扣除张三10个金币  
例如 【#设置 @张三 金币 20】 将张三的金币设置为20
后两个需要管理员权限（非群管理员权限，需在机器人后台设置）""",
            # 上面所有的东西 帮助 <模块名>
            "pluginver": 3,
            "type": "group"
        }

    def __init__(self, setbot, moduleall=None, db=None):
        "这里主要是模块自身的初始化"
        bot = setbot
        self.mod = moduleall
        self.data = {}


def this():
    return jifen

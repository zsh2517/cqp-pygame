import time
import botbasic
import config
from aiocqhttp import *
import os
import json

bot = CQHttp()
mod = []


# 所有程序都在处理中
@bot.on_message('private')
@bot.on_message('group')
async def _(event: Event):
    message, group_id, user_id = botbasic.getmsg_full(event)
    # print(message)
    flag = False
    if event.detail_type == "group":
        if botbasic.if_group_enabled(event.group_id) and \
                (not botbasic.if_ban(group_id, user_id)):
            # (event.message.find("[CQ:at,qq=2772183014]") != -1):
            # 更换了响应方式，所以这里就不需要@了
            # 如果确实存在了的话
            flag = True
        else:
            flag = False
    else:
        flag = True
    if flag == False:
        return
    for i in range(0, len(mod)):
        id = ""
        if mod[i]["info"]["type"] == "global":
            id = "global"
            pass
        elif mod[i]["info"]["type"] == "group":
            if group_id == None:
                id = "group-user" + str(user_id)
            else:
                id = "group" + str(group_id)
            pass
        elif mod[i]["info"]["type"] == "user-global":
            id = "user-global" + str(user_id)
            pass
        elif mod[i]["info"]["type"] == "user":
            id = "user-singal" + str(group_id) + "-" + str(user_id)
        else:
            # not support
            pass
            # 上面处理消息是否可以被接受
        if (id not in mod[i]["instance"].keys()):
            if (mod[i]["info"]["pluginver"] >= 2):
                mod[i]["instance"][id] = mod[i]["module"].this()(
                    setbot=bot, moduleall=mod, db=None)
            else:
                mod[i]["instance"][id] = mod[i]["module"].this()(
                    setbot=bot, db=None)
        ret = await mod[i]["instance"][id].check(event=event)
        # 先不去做独占模式了，因为不同地脚本地运行不一样
        if ret == 0:  # no reply
            continue
        elif ret == 1:
            continue
        elif ret == 2:
            await mod[i]["instance"][id].reply(event)


if __name__ == '__main__':
    # while True:
    try:
        savedata = ""
        find_savedata = False
        if os.path.exists("data.json"):
            print("发现保存数据")
            f = open("data.json", "r", encoding="utf-8")
            savedata = json.load(f)
            find_savedata = True
        # 载入模块
        for root, dirs, files in os.walk("./module/", topdown=False):
            for name in files:
                if name[-3:] == ".py":
                    m = os.path.join(root, name).replace(
                        "./", "").replace("/", ".").replace(".py", "")
                    print("发现模块: " + m)
                    exec("import " + m)
                    exec("x = " + m)
                    # print(x)
                    info = x.this().class_info()
                    sign = info["sign"]
                    print("载入模块[%s](%s)成功，正在读取数据" % (info["name"], sign))
                    ins = {}
                    if find_savedata and info["pluginver"] >= 3 and (sign in savedata.keys()):
                        for key in savedata[sign]["instance"].keys():
                            ins[key] = x.this()(setbot=bot, moduleall=mod, db=None)
                            ins[key].importdata(savedata[sign]["instance"][key])
                    mod.append({
                        "module": x,
                        "info": info,
                        "instance": ins,
                    })
        # 运行
        botbasic.setbot(bot)
        bot.run(host=config.cqhttp_ws["host"],
                port=config.cqhttp_ws["port"], debug=True)
    except KeyboardInterrupt as exc:
        botbasic.savedata(mod)

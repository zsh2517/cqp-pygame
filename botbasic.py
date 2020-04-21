import config
from aiocqhttp import *
import json

bot = CQHttp()


def setbot(mainbot):
    global bot
    bot = mainbot


def if_group_enabled(group):
    if group in config.group:
        return True
    return False


def if_admin(group, user):
    if not if_group_enabled(group):
        return False
    if user not in config.group_conf[group]["admin"]:
        return False
    return True


def if_ban(group, user):
    if not if_group_enabled(group):
        return False
    if user not in config.group_conf[group]["ban"]:
        return False
    return True


def admin(group, user, enable):
    # 修改成功是True，未修改或者修改失败是False
    x = if_admin(group, user)
    if x == enable:
        return False
    if not if_group_enabled(group):
        return False
    if enable:
        config.group_conf[group]["admin"].add(user)
    else:
        config.group_conf[group]["admin"].remove(user)


def ban(group, user, enable):
    # 成功是True，失败是False
    # 修改成功是True，未修改或者修改失败是False
    x = if_ban(group, user)
    if x == enable:
        return False
    if not if_group_enabled(group):
        return False
    if enable:
        config.group_conf[group]["ban"].add(user)
    else:
        config.group_conf[group]["ban"].remove(user)


def simple_available(group, user):
    return not if_ban(group, user)


async def reply(event, text, at=True):
    text = str(text)
    if event.detail_type == "group":
        if at:
            await bot.send_group_msg(group_id=event.group_id, message="[CQ:at,qq={0}] ".format(event.user_id) + text,
                                     auto_escape=False)
        else:
            await bot.send_group_msg(group_id=event.group_id, message=text, auto_escape=False)
    elif event.detail_type == "private":
        await bot.send_private_msg(user_id=event.user_id, message=text,
                                   auto_escape=False)


def getmsg(event):
    message = event.message.replace("[CQ:at,qq=2772183014]", "")
    while (message[0] == " "):
        message = message[1:]
    return message


def getmsg_full(event):
    message = event.message.replace("[CQ:at,qq=2772183014]", "")
    while (message[0] == " "):
        message = message[1:]
    user_id = event.user_id
    group_id = event.group_id
    return message, group_id, user_id



def savedata(mod):
    print("准备保存数据")
    savedata = {}
    for i in range(0, len(mod)):
        if mod[i]["info"]["pluginver"] >= 3:
            sign = mod[i]["info"]["sign"]
            temp = {}
            savedata[sign] = {}
            savedata[sign]["info"] = mod[i]["info"]
            savedata[sign]["instance"] = {}
            for key in mod[i]["instance"].keys():
                savedata[sign]["instance"][key] = mod[i]["instance"][key].exportdata()
            print("模块[%s](%s)保存完成" %
                    (mod[i]["info"]["name"], mod[i]["info"]["sign"]))
    f = open("data.json", "w", encoding="utf-8")
    # json.dump(savedata, f, ensure_ascii=False)
    f.write(json.dumps(savedata, ensure_ascii=False))
    f.close()
    print("保存完成")

def text_share(url, title, content, image):
    text = "[CQ:share,url={0},title={1},content={2},image={3}]"
    text = text.format(url, title, content, image)
    return text

def music_share(url, audio, title, content, image):
    return "[CQ:music,type=custom,url={0},audio={1},title={2},content={3},image={4}]".format(url, audio, title, config, image)

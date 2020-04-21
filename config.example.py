# websocket监听设置
cqhttp_ws = {
    "host": "0.0.0.0",
    "port": 5000
}

# 数据库配置
# 不支持数据库....这一项没用
# db = {
#     "type": "sqlite3",
#     # 可选择的数据库类型: mysql sqlite3
#     "host": "",
#     # 如果使用sqlite3，那么这里host写文件地址，然后port不写
#     "port": 3306,
#     "username": "",
#     "password": "",
#     "database": ""
# }

# 群设置（激活的群）
# group = {761245269}
# group = set()
group = {
    1234567890,  # 第一个群群号
    2345678901   # 第二个群群号
}
group_conf = {
    1234567890: {
        "admin": set(),
        # admin 为管理员，具有更高的权限（如果插件支持的话）
        "ban": set()
        # ban 为封禁人员，机器人不会响应他的信息
    },
    2345678901: {
        "admin": set(),
        "ban": set()
    }
}

import json
import requests
from flask import request, Flask
from officialGPT import Chatbot

cqhttp_url = "http://localhost:8700" # CQ-http地址
qq_no = "0" # 机器人QQ号，记得修改
port = 10016 # ChatGPT端口号
api_key = ""
temperature = 0.5

# 创建一个服务，把当前这个python文件当做一个服务
server = Flask(__name__)
# 创建ChatGPT实例
chatbot = Chatbot(api_key=api_key)

# 与ChatGPT交互的方法
def chat(msg):
    response = chatbot.ask(msg, temperature=temperature)
    message = response['choices'][0]['text']
    print("ChatGPT返回内容: ")
    print(message)
    return message

# 测试接口，可以用来测试与ChatGPT的交互是否正常，用来排查问题
@server.route('/chat', methods=['post'])
def chatapi():
    requestJson = request.get_data()
    if requestJson is None or requestJson == "" or requestJson == {}:
        resu = {'code': 1, 'msg': '请求内容不能为空'}
        return json.dumps(resu, ensure_ascii=False)
    data = json.loads(requestJson)
    print(data)
    try:
        msg = chat(data['msg'])
    except Exception as error:
        print("接口报错")
        resu = {'code': 1, 'msg': '请求异常: ' + str(error)}
        return json.dumps(resu, ensure_ascii=False)
    else:
        resu = {'code': 0, 'data': msg}
        return json.dumps(resu, ensure_ascii=False)


# 测试接口，可以测试本代码是否正常启动
@server.route('/', methods=["GET"])
def index():
    return f"你好，QQ机器人逻辑处理端已启动<br/>"


# qq消息上报接口，qq机器人监听到的消息内容将被上报到这里
@server.route('/', methods=["POST"])
def get_message():
    if request.get_json().get('message_type') == 'private':  # 如果是私聊信息
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        sender = request.get_json().get('sender')  # 消息发送者的资料
        print("收到私聊消息：")
        print(message)
        # 下面你可以执行更多逻辑，这里只演示与ChatGPT对话
        msg_text = chat(message)  # 将消息转发给ChatGPT处理
        send_private_message(uid, msg_text)  # 将消息返回的内容发送给用户
    if request.get_json().get('message_type') == 'group':  # 如果是群消息
        gid = request.get_json().get('group_id')  # 群号
        uid = request.get_json().get('sender').get('user_id')  # 发言者的qq号
        message = request.get_json().get('raw_message')  # 获取原始信息
        message_id = request.get_json().get('message_id') # 获取消息id

        # 判断当被@时才回答
        if str("[CQ:at,qq=%s]"%qq_no) in message:
            sender = request.get_json().get('sender')
            print("收到群聊消息：")
            print(message)
            # 下面你可以执行更多逻辑，这里只演示与ChatGPT对话
            msg_text = chat(message)  # 将消息转发给ChatGPT处理
            msg_text = str('[CQ:reply,id=%s]'%message_id) + str(msg_text)  # 引用回复
            send_group_message(gid, msg_text)  # 将消息转发到群里
    if request.get_json().get('post_type') == 'request':  # 收到请求消息
        print("收到请求消息")
        request_type = request.get_json().get('request_type')  # group
        uid = request.get_json().get('user_id')
        flag = request.get_json().get('flag')
        comment = request.get_json().get('comment')
        if request_type == "friend":
            print("收到加好友申请")
            print("QQ：", uid)
            print("验证信息", comment)
            # 直接同意，你可以自己写逻辑判断是否通过
            set_friend_add_request(flag, "true")
        if request_type == "group":
            print("收到群请求")
            sub_type = request.get_json().get('sub_type')  # 两种，一种的加群(当机器人为管理员的情况下)，一种是邀请入群
            gid = request.get_json().get('group_id')
            if sub_type == "add":
                # 如果机器人是管理员，会收到这种请求，请自行处理
                print("收到加群申请，不进行处理")
            elif sub_type == "invite":
                print("收到邀请入群申请")
                print("群号：", gid)
                # 直接同意，你可以自己写逻辑判断是否通过
                set_group_invite_request(flag, "true")
    return "ok"


# 发送私聊消息方法 uid为qq号，message为消息内容
def send_private_message(uid, message):
    try:
        res = requests.post(url=cqhttp_url + "/send_private_msg",
                            params={'user_id': int(uid), 'message': message}).json()
        if res["status"] == "ok":
            print("私聊消息发送成功")
        else:
            print(res)
            print("私聊消息发送失败，错误信息：" + str(res['wording']))

    except:
        print("私聊消息发送失败")


# 发送群消息方法
def send_group_message(gid, message):
    try:
        res = requests.post(url=cqhttp_url + "/send_group_msg",
                            params={'group_id': int(gid), 'message': message}).json()
        if res["status"] == "ok":
            print("群消息发送成功")
        else:
            print("群消息发送失败，错误信息：" + str(res['wording']))
    except:
        print("群消息发送失败")


# 处理好友请求
def set_friend_add_request(flag, approve):
    try:
        requests.post(url=cqhttp_url + "/set_friend_add_request", params={'flag': flag, 'approve': approve})
        print("处理好友申请成功")
    except:
        print("处理好友申请失败")


# 处理邀请加群请求
def set_group_invite_request(flag, approve):
    try:
        requests.post(url=cqhttp_url + "/set_group_add_request",
                      params={'flag': flag, 'sub_type': 'invite', 'approve': approve})
        print("处理群申请成功")
    except:
        print("处理群申请失败")


if __name__ == '__main__':
    server.run(port=port, host='0.0.0.0')

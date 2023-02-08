# QQ机器人版的ChatGPT(Docker)

[![Docker Stars](https://img.shields.io/docker/stars/tylearymf/chatgpt-qqbot.svg)](https://hub.docker.com/r/tylearymf/chatgpt-qqbot)
[![Docker Pulls](https://img.shields.io/docker/pulls/tylearymf/chatgpt-qqbot.svg)](https://hub.docker.com/r/tylearymf/chatgpt-qqbot)

Github主页: [chatgpt-qqbot](https://github.com/tylearymf/chatgpt-qqbot)

# 2023.2.6可用

## 创建volume

```
sudo docker volume create qqbot
```

## 创建容器

* QQ_NUMBER: 目标QQ号（必填）
* QQ_PASSWORD: QQ密码（可选）
  * 如果该项不设置时，则使用目标QQ号扫描二维码登录，但是必须保证docker运行网络与扫码手机所在网络是同一个IP段内
* CHATGPT_API_KEY: 从这里 [api-keys](https://platform.openai.com/account/api-keys)获取一个key填入即可.（必填）
* LISTEN_PORT: 8700 (可选)
* POST_PORT: 10016 (可选)

```
扫码登录版：sudo docker run -it -v qqbot:/app --name=qqbot -e LISTEN_PORT=8700 -e POST_PORT=10016 -e QQ_NUMBER=123456 -e CHATGPT_API_KEY=xxx tylearymf/chatgpt-qqbot latest

QQ密码登录版：sudo docker run -it -v qqbot:/app --name=qqbot -e LISTEN_PORT=8700 -e POST_PORT=10016 -e QQ_NUMBER=123456 -e QQ_PASSWORD=xxx -e CHATGPT_API_KEY=xxx tylearymf/chatgpt-qqbot latest
```

用其他QQ向目标QQ发送消息即可测试ChatGPT了。

## 引用

- [ChatGPT](https://github.com/acheong08/ChatGPT)
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [憨憨的OpenGPT 搭建 QQ 机器人](https://blog.hanhanz.top/?p=195)

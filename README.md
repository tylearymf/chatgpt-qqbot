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

* QQ_NUMBER: 目标QQ号

* CHATGPT_API_KEY: 从这里 [api-keys](https://platform.openai.com/account/api-keys)获取一个key填入即可.
* LISTEN_PORT: 8700 (默认值)
* POST_PORT: 10016 (默认值)

```
sudo docker run -it -v qqbot:/app --name=qqbot -e LISTEN_PORT=8700 -e POST_PORT=10016 -e QQ_NUMBER=123456 -e CHATGPT_API_KEY=xxx tylearymf/chatgpt-qqbot latest
```

运行后打开QQ扫描二维码登录（需要用目标QQ号扫描），登录成功后，下次会自动登录

用其他QQ向目标QQ发送消息即可测试ChatGPT了。

## 二次启动容器

```
sudo docker start qqbot
```

## 引用

- [ChatGPT](https://github.com/acheong08/ChatGPT)
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)
- [憨憨的OpenGPT 搭建 QQ 机器人](https://blog.hanhanz.top/?p=195)

import os

qq_number = os.environ.get("QQ_NUMBER", "")
qq_password = os.environ.get("QQ_PASSWORD", "")
chatgpt_api_key = os.environ.get("CHATGPT_API_KEY", "")
listen_port = os.environ.get("LISTEN_PORT", "")
post_port = os.environ.get("POST_PORT", "")

if qq_number == "":
    raise Exception("QQ Number 未设置.")

if chatgpt_api_key == "":
    raise Exception("CHATGPT_API_KEY 未设置.")

config_name = "config.yml"
bot_script_name = "qqbot.py"

with open(config_name, "r") as f:
    config_content = f.read()

with open(bot_script_name, "r") as f:
    bot_content = f.read()

bot_content = bot_content.replace('qq_no = "0"', 'qq_no = "' + qq_number +'"')
bot_content = bot_content.replace('api_key = ""', 'api_key = "' + chatgpt_api_key + '"')

if  listen_port != "":
    config_content = config_content.replace("address: 0.0.0.0:8700", "address: 0.0.0.0:" + listen_port)
    bot_content = bot_content.replace('cqhttp_url = "http://localhost:8700"', 'cqhttp_url = "http://localhost:' + listen_port + '"')

if  post_port != "":
    config_content = config_content.replace("url: http://127.0.0.1:10016", "url: http://127.0.0.1:" + post_port)
    bot_content = bot_content.replace('port = 10016', 'port = ' + post_port)

if qq_number != "":
    config_content = config_content.replace("uin: 0", "uin: " + qq_number)

if qq_password != "":
    config_content = config_content.replace("password: ''", "password: '" + qq_password + "'")

with open(config_name, "w") as f:
    f.write(config_content)

with open(bot_script_name, "w") as f:
    f.write(bot_content)

bot_cmd = 'python qqbot.py'
os.popen(bot_cmd)

qq_cmd = "./go-cqhttp/go-cqhttp"
os.system('chmod +x ' + qq_cmd)
os.system(qq_cmd)
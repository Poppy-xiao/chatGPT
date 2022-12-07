from pathlib import Path
from hoshino import Service, priv, aiorequests, R
import requests
import base64
from PIL import Image
from io import BytesIO
import math
import random
import hoshino
import asyncio
from revChatGPT.revChatGPT import Chatbot
from hoshino import Service, priv, aiorequests, R
from qbittorrent import Client  

config = {
        "Authorization": "<Your Bearer Token Here>", # This is optional
        "session_token": "<Your Token Here>"
}

user_session = dict()
chatbot = Chatbot(config)

sv_help = """ gpt + 内容可以发送聊天
"""
sv = Service(
    name="chatGPT",  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    bundle="娱乐",  # 分组归类
    help_=sv_help  # 帮助说明
) 

def get_chat_response(prompt): 
    try:
        chatbot.reset_chat()
        resp = chatbot.get_chat_response(prompt)
        return resp['message']
    except Exception as e:
        print(e)
        return f"发生错误: {str(e)}"
 

@sv.on_prefix(("gpt"))
async def chatGPT_method(bot, ev): 
    uid = ev.user_id
    gid = ev.group_id
    name = ev.sender['nickname'] 
    msg = str(ev.message.extract_plain_text()).strip()
    resp = await asyncio.get_event_loop().run_in_executor(None, get_chat_response, msg)
    await bot.send(ev, resp, at_sender = True)
 
from hoshino import Service, priv 
import asyncio
from revChatGPT.revChatGPT import Chatbot
import time

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


def get_chat_response(session_id, prompt):
    if session_id in user_session:
        # 如果在三分钟内再次发起对话则使用相同的会话ID
        if time.time() < user_session[session_id]['timestamp'] + 60 * 3:
            chatbot.conversation_id = user_session[session_id]['conversation_id']
            chatbot.parent_id = user_session[session_id]['parent_id']
        else:
            chatbot.reset_chat()
    else:
        chatbot.reset_chat() 
    try:
        resp = chatbot.get_chat_response(prompt, output="text") 
        user_cache = dict()
        user_cache['timestamp'] = time.time()
        user_cache['conversation_id'] = resp['conversation_id']
        user_cache['parent_id'] = resp['parent_id']
        user_session[session_id] = user_cache

        return resp['message']
    except Exception as e:
        return f"发生错误: {str(e)}"
 

@sv.on_prefix(("gpt"))
async def chatGPT_method(bot, ev): 
    uid = ev.user_id
    gid = ev.group_id
    name = ev.sender['nickname'] 
    msg = str(ev.message.extract_plain_text()).strip()
    resp = await asyncio.get_event_loop().run_in_executor(None, get_chat_response, uid, msg)
    await bot.send(ev, resp, at_sender = True)

 # 定时刷新seesion_token
@sv.scheduled_job("interval", minutes=10)
async def refresh_session(): 
    chatbot.refresh_session()
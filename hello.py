from telethon import TelegramClient, sync
import os
from vendor.class_bot import LYClass  # 导入 LYClass
import asyncio
import time
import re

# 检查是否在本地开发环境中运行
if not os.getenv('GITHUB_ACTIONS'):
    from dotenv import load_dotenv
    load_dotenv()

# 从环境变量中获取值
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
session_name = api_id+'session_name'  # 确保与上传的会话文件名匹配

# 创建客户端
client = TelegramClient(session_name, api_id, api_hash)

# 创建 LYClass 实例
ly_class_instance = LYClass('text')

# 定义机器人信息和正则表达式
wp_bot = [
    {
        'title': 'blgg',
        'bot_name': 'FilesDrive_BLGG_bot',
        'id': '6995324980',  # 6854050358
        'mode': 'enctext',
        'pattern': r'(?:p_|vi_|f_|fds_|pk_)[a-zA-Z0-9-_]{30,100}\b',
        'message_thread_id': '23'
    },
    {
        'title': 'filesave',
        'bot_name': 'FileSaveNewBot',
        'id': '7008164392',  # 6854050358
        'mode': 'enctext',
        'pattern': r'(?:P_|V_|D_)[a-zA-Z0-9-_]{15,29}\b',
        'message_thread_id': '25'
    },
    {
        'title': 'showfiles',
        'bot_name': 'ShowFilesBot',
        'id': '6976547743',  # 6854050358
        'mode': 'enctext',
        'pattern': r'(?:showfilesbot_|fds_|pk_)[a-zA-Z0-9-_]{15,29}\b',
        'message_thread_id': '27'
    },
    {
        'title': 'datapan',
        'bot_name': 'datapanbot',
        'id': '6854050358',  # 6854050358
        'mode': 'enctext',
        'pattern': r'(?:P_DataPanBot_|V_DataPanBot_|D_DataPanBot_|fds_|pk_)[a-zA-Z0-9-_]{30,100}\b',
        'message_thread_id': '28'
    },
    {
        'title': 'filetobot',
        'bot_name': 'filetobot',
        'id': '291481095',
        'mode': 'link',
        'pattern': r'https:\/\/t\.me\/filetobot\?start=(\w{14,20})',
        'message_thread_id': '29'
    },
    {
        'title': 'filein',
        'bot_name': 'fileinbot',
        'id': '1433650553',
        'mode': 'link',
        'pattern': r'https:\/\/t\.me\/fileinbot\?start=(\w{14,20})',
        'message_thread_id': '30'
    },
    {
        'title': 'fileoffrm',
        'bot_name': 'fileoffrm_bot',
        'id': '7085384480',
        'mode': 'link',
        'pattern': r'https:\/\/t\.me\/fileoffrm_bot\?start=(\w{14,20})',
        'message_thread_id': '31'
    },
    {
        'title': 'wangpan',
        'bot_name': 'wangpanbot',
        'id': '5231326048',
        'mode': 'link',
        'pattern': r'https:\/\/t\.me\/WangPanBOT\?start=(file\w{14,20})',
        'message_thread_id': '32'
    }
]

# 定义匹配函数
def match_pattern(input_str):
    for bot in wp_bot:
        if re.search(bot['pattern'], input_str):
            return bot['title']
    return None


# 定义消息处理函数
async def process_message(message):
    try:
        await asyncio.sleep(3)
        # print(f"Processing message: {message}\n")
        print(f"Processing message: {message.id}\n")

        title = match_pattern(message.text)

        if title:
            handler = getattr(ly_class_instance, title, None)
            if handler:
                if asyncio.iscoroutinefunction(handler):
                    await handler(client, message)
                else:
                    handler(message)
            else:
                print(f"No handler found for title: {title}\n")
        else:
            print(f"No matching pattern for message: {message.text}\n")

    except Exception as e:
        print(f"An error occurred while processing message: {e}\n")

async def main():
    await client.start(phone_number)

    # 使用指定的 chat_id
    chat_id = -1001939978944
    ly_class_instance.chat_id = chat_id

    start_time = time.time()
    while True:
        # 获取最近3条消息
        async for message in client.iter_messages(chat_id, limit=3):
            await process_message(message)
        
        # 检查累计执行时间是否超过5分钟
        elapsed_time = time.time() - start_time
        if elapsed_time > 900:  # 300秒等于15分钟
            print("Execution time exceeded 5 minutes. Stopping.")
            break
        else:
            print("Execution time is "+str(elapsed_time)+" seconds. Continuing... after 60 seconds.")
        
        await asyncio.sleep(60)  # 间隔30秒

    
            

with client:
    client.loop.run_until_complete(main())

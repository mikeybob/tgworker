from telethon import TelegramClient, sync
import os
from vendor.class_bot import LYClass  # 导入 LYClass

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

async def main():
    await client.start(phone_number)

    chat_id = -1001717350482  # 替换为你的chat_id
    message_thread_id = 50047  # 替换为你的message_thread_id

    # 获取消息
    async for message in client.iter_messages(chat_id, reply_to=message_thread_id):
        print(message.sender_id, message.text)

with client:
    client.loop.run_until_complete(main())

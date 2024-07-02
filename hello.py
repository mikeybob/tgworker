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
session_name = api_id + 'session_name'  # 确保与上传的会话文件名匹配

# 创建客户端
client = TelegramClient(session_name, api_id, api_hash)

# 创建 LYClass 实例
ly_class_instance = LYClass('text')

# 定义消息处理函数
async def process_message(message):
    try:
        print(f"Processing message: {message.id}")
        if message.reply_to:
            print(f"Message has reply_to: {message.reply_to.reply_to_msg_id}")
        if message.reply_to and message.reply_to.reply_to_msg_id == 1:
            ly_class_instance.ab(message)
        elif message.reply_to and message.reply_to.reply_to_msg_id == 2:
            ly_class_instance.cd(message)
        elif message.reply_to and message.reply_to.reply_to_msg_id == 50047:
            print("Calling datapan method...")
            await ly_class_instance.datapan(client, message)  # 传入 client 实例和 message
        else:
            print(f"Unhandled thread ID: {message.reply_to.reply_to_msg_id if message.reply_to else 'None'} - Message: {message.sender_id}, {message.text}")
    except Exception as e:
        print(f"An error occurred while processing message: {e}")

async def main():
    await client.start(phone_number)

    # 使用指定的 chat_id
    chat_id = -1001717350482

    

    # 获取最近100条消息
    async for message in client.iter_messages(chat_id, limit=3):
        if message.reply_to:
            await process_message(message)

with client:
    client.loop.run_until_complete(main())

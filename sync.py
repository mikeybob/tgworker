from telethon import TelegramClient
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


try:
    config = {
        'api_id': os.getenv('API_ID'),
        'api_hash': os.getenv('API_HASH'),
        'phone_number': os.getenv('PHONE_NUMBER'),
        'session_name': os.getenv('API_ID') + 'session_name',
        'work_bot_id': os.getenv('WORK_BOT_ID'),
        'work_chat_id': int(os.getenv('WORK_CHAT_ID', 0)),  # 默认值为0
        'public_bot_id': os.getenv('PUBLIC_BOT_ID'),
        'warehouse_chat_id': int(os.getenv('WAREHOUSE_CHAT_ID', 0)),  # 默认值为0
        'link_chat_id': int(os.getenv('LINK_CHAT_ID', 0))
    }

    # 创建 LYClass 实例
    tgbot = LYClass(client,config)
    
   
except ValueError:
    print("Environment variable WORK_CHAT_ID or WAREHOUSE_CHAT_ID is not a valid integer.")
    exit(1)
    
#max_process_time 設為 1200 秒，即 20 分鐘
max_process_time = 1200  # 20分钟
max_media_count = 25  # 10个媒体文件
max_count_per_chat = 5  # 每个对话的最大消息数

async def main():
    await client.start(phone_number)

    botlist = ['@ztdMiWen005Bot','@ztdStone005BOT']  
        # //,7452636047,7075620315,6588695181,6373803154,6086006554
   
    for bot_id in botlist:
        try:
            await tgbot.client.send_message(bot_id, "/start")
        #    // await tgbot.client.send_message(bot_id, str(bot_id))
        except Exception as e:
            print(f"Error sending message to work_bot_id: {e}")
            continue
    


with client:
    client.loop.run_until_complete(main())

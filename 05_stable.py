from telethon import TelegramClient, sync
import os
from vendor.class_bot import LYClass  # 导入 LYClass
from vendor.wpbot import wp_bot  # 导入 wp_bot
import asyncio
import time
import re
from telethon.tl.types import InputMessagesFilterEmpty,Message

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



# 定义匹配函数
def match_pattern(input_str):
    for bot in wp_bot:
        if re.search(bot['pattern'], input_str):
            return bot
    return None


# 定义消息处理函数
async def process_message(message):
    try:
        # print(f"Processing message: {message}\n")
        print(f"Processing message: {message.id}\n")

        if message.text:

            bot = match_pattern(message.text)
            title = bot['title'] if bot else None

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
            print(f"No matching pattern for message: {message.text} {message} \n")

    except Exception as e:
        print(f"An error occurred while processing message: {e} \n message:{message}\n")
    finally:
         await asyncio.sleep(3)

async def main():
    await client.start(phone_number)

     # 获取并处理频道实体
    try:
        # chat_id = -1001507154171    #OLD
        chat_id = -1001951775419
        # chat_id = -1001971784803    #TEST
        entity = await client.get_entity(chat_id)
        ly_class_instance.chat_id = entity.id
    except ValueError as e:
        print(f"Failed to get entity for chat_id {chat_id}: {e}")
        return

    start_time = time.time()
    while True:
        # 获取指定范围内的消息，最多读取20条
        async for message in client.iter_messages(entity, limit=20, reverse=True,filter=InputMessagesFilterEmpty()):
            if message.text:
                await process_message(message)
          

        # 检查累计执行时间是否超过15分钟
        elapsed_time = time.time() - start_time
        if elapsed_time > 1200:  #1200秒等于20分钟
            print("Execution time exceeded 5 minutes. Stopping.")
            break
        else:
            print("Execution time is "+str(elapsed_time)+" seconds. Continuing... after 200 seconds.")
        
        await asyncio.sleep(200)  # 间隔200秒

with client:
    client.loop.run_until_complete(main())

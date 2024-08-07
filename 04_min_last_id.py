from telethon import TelegramClient, sync
import os
from vendor.class_bot import LYClass,wp_bot,save_last_read_message_id,load_last_read_message_id  # 导入 LYClass
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



# 定义匹配函数
def match_pattern(input_str):
    for bot in wp_bot:
        if re.search(bot['pattern'], input_str):
            return bot['title']
    return None


# 定义消息处理函数
async def process_message(message):
    try:
       
        # print(f"Processing message: {message}\n")
        print(f"Processing message: {message.id}\n")

        if message.text:

            title = match_pattern(message.text)

            if title:
                handler = getattr(ly_class_instance, title, None)
                if handler:
                    
                    if asyncio.iscoroutinefunction(handler):
                        print(f"iscoroutinefunction\n")
                        await handler(client, message)
                    else:
                        print(f"none-iscoroutinefunction\n")
                        handler(message)
                else:
                    print(f"No handler found for title: {title}\n")
        else:
            print(f"No matching pattern for message: {message.text} {message} \n")

        # 处理完消息后，保存最后读取的消息 ID
        save_last_read_message_id(message.peer_id.channel_id, message.id)


    except Exception as e:
        print(f"An error occurred while processing message: {e} {message}\n")
    finally:
         await asyncio.sleep(3)

async def main():
    await client.start(phone_number)

     # 获取并处理频道实体
    try:
        chat_id = -1001507154171
        entity = await client.get_entity(chat_id)
        ly_class_instance.chat_id = entity.id
    except ValueError as e:
        print(f"Failed to get entity for chat_id {chat_id}: {e}")
        return

    # 加载最后读取的消息 ID
    last_read_message_id = load_last_read_message_id(entity.id)
  
    # 获取最新的消息 ID
    latest_message = await client.get_messages(entity, limit=1)
    latest_message_id = latest_message[0].id if latest_message else 0


    start_time = time.time()
    while True:
        # 获取指定范围内的消息，最多读取20条
        async for message in client.iter_messages(entity, min_id=last_read_message_id, max_id=latest_message_id, limit=20, reverse=True):
            await process_message(message)

        # 更新最后读取的消息 ID
        if latest_message_id > last_read_message_id:
            last_read_message_id = latest_message_id
        
        # 检查累计执行时间是否超过5分钟
        elapsed_time = time.time() - start_time
        if elapsed_time > 900:  # 900秒等于15分钟
            print("Execution time exceeded 5 minutes. Stopping.")
            break
        else:
            print("Execution time is "+str(elapsed_time)+" seconds. Continuing... after 60 seconds.")
        
        await asyncio.sleep(200)  # 间隔200秒

    
            

with client:
    client.loop.run_until_complete(main())

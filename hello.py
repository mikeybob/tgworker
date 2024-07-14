from telethon import TelegramClient, sync
import os
from vendor.class_bot import LYClass  # 导入 LYClass
from vendor.wpbot import wp_bot  # 导入 wp_bot
import asyncio
import time
import re
from telethon.tl.types import InputMessagesFilterEmpty, Message, User, Chat, Channel

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
try:
    ly_class_instance.work_bot_id = os.getenv('WORK_BOT_ID')
    ly_class_instance.work_chat_id = int(os.getenv('WORK_CHAT_ID'))
    ly_class_instance.public_bot_id = os.getenv('PUBLIC_BOT_ID')
    ly_class_instance.warehouse_chat_id = int(os.getenv('WAREHOUSE_CHAT_ID'))
except ValueError:
    print("Environment variable WORK_CHAT_ID or WAREHOUSE_CHAT_ID is not a valid integer.")
    exit(1)

max_process_time = 1200  # 20分钟
max_media_count = 10  # 2个媒体文件


# 定义匹配函数
def match_pattern(input_str):
    for bot in wp_bot:
        if re.search(bot['pattern'], input_str):
            return bot
    return None

async def forward_encstr_to_encbot(message):
    try:
        enc_exist = False
        print(f">>Processing message(1): {message.id}\n")
        if message.text:
            for bot in wp_bot:
                pattern = re.compile(bot['pattern'])
                matches = pattern.findall(message.text)
                for match in matches:
                    enc_exist=True
                    async with client.conversation(ly_class_instance.work_bot_id) as conv:
                        await conv.send_message(match)
                        print(match)
        else:
            print(f"No matching pattern for message: {message.text} {message} \n")
    except Exception as e:
        print(f"An error occurred while processing message: {e} \n message:{message}\n")
    finally:
        if enc_exist:
            await asyncio.sleep(3)
        else:
            await asyncio.sleep(0)

async def forward_media_to_warehouse(message):
    try:
        print(f">>Processing message(2): {message.id}\n")
        if message.media:
            if message.chat_id != ly_class_instance.warehouse_chat_id:
                last_message_id = await ly_class_instance.send_message(client, message)
                return last_message_id
            else:
                print(f"Message is from warehouse chat, not forwarding: {message.id}\n")
        else:
            print(f"No matching pattern for message: {message.text} {message} \n")
    except Exception as e:
        print(f"An error occurred while processing message: {e} \n message:{message}\n")
    finally:
        await asyncio.sleep(3)
    return message.id

# 定义消息处理函数
async def fetch_media_from_enctext(message):
    try:
        print(f">>Processing message(3): {message.id}\n")
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
        if title:
            await asyncio.sleep(3)
        else:
            await asyncio.sleep(0)

async def main():
    await client.start(phone_number)
    
    try:
        entity = await client.get_entity(ly_class_instance.work_chat_id)
        ly_class_instance.chat_id = entity.id
    except ValueError as e:
        print(f"Failed to get entity for chat_id {ly_class_instance.work_chat_id}: {e}")
        return

    start_time = time.time()
    media_count = 0
    while True:
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            this_chat_id = '-100'+str(entity.id)
            # 跳过来自 WAREHOUSE_CHAT_ID 的对话
            if this_chat_id == str(ly_class_instance.warehouse_chat_id):
                continue
            if str(entity.id) == '1838623494':
                continue
                
                
           
            # 打印处理的实体名称（频道或群组的标题）
            if isinstance(entity, Channel) or isinstance(entity, Chat):
                entity_title = entity.title
            elif isinstance(entity, User):
                entity_title = f'{entity.first_name or ""} {entity.last_name or ""}'.strip()
            else:
                entity_title = f'Unknown entity {entity.id}'
                
            print(f"\nProcessing entity: {this_chat_id} - {entity_title}\n")

            if dialog.unread_count >= 0 and (dialog.is_user or dialog.is_group or dialog.is_channel):
                last_read_message_id = ly_class_instance.load_last_read_message_id(entity.id)

                print(f">Reading messages from entity {entity.id} - {last_read_message_id}\n")
                async for message in client.iter_messages(entity, min_id=last_read_message_id, limit=30, reverse=True, filter=InputMessagesFilterEmpty()):
                    last_message_id = message.id  # 初始化 last_message_id
                    
                    if message.text:
                        last_message_id = message.id
                        tme_links = re.findall(r'me/\+[a-zA-Z0-9_\-]{15,17}|me/joinchat/[a-zA-Z0-9_\-]{15,18}', message.text)
                       
                        if tme_links:
                            for link in tme_links:
                                await ly_class_instance.join_channel_from_link(client, "https://t."+link)
                            # 跳过后续处理
                        elif entity.id == ly_class_instance.chat_id:
                            await fetch_media_from_enctext(message)
                        elif dialog.is_group or dialog.is_channel:
                            await forward_encstr_to_encbot(message)
                    elif message.media:
                        if entity.id != ly_class_instance.chat_id:
                            last_message_id = await forward_media_to_warehouse(message)
                            media_count = media_count + 1
                    ly_class_instance.save_last_read_message_id(entity.id, last_message_id)
                    if media_count >= max_media_count:
                        break


            elapsed_time = time.time() - start_time
            if elapsed_time > max_process_time:  # 1200秒等于20分钟
                print(f"Execution time exceeded {max_process_time} seconds. Stopping.")
                break
            if media_count >= max_media_count:
                print(f"Media count exceeded {max_media_count}. Stopping.\n")
                break


        print("Execution time is " + str(elapsed_time) + " seconds. Continuing next cycle... after 200 seconds.")
        await asyncio.sleep(200)  # 间隔200秒

with client:
    client.loop.run_until_complete(main())

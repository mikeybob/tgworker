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


try:
    config = {
        'api_id': os.getenv('API_ID'),
        'api_hash': os.getenv('API_HASH'),
        'phone_number': os.getenv('PHONE_NUMBER'),
        'session_name': os.getenv('API_ID') + 'session_name',
        'work_bot_id': os.getenv('WORK_BOT_ID'),
        'work_chat_id': (os.getenv('WORK_CHAT_ID')),
        'public_bot_id': os.getenv('PUBLIC_BOT_ID'),
        'warehouse_chat_id': (os.getenv('WAREHOUSE_CHAT_ID')),
        'link_chat_id': (os.getenv('LINK_CHAT_ID'))
    }
    # 创建 LYClass 实例
    tgbot = LYClass(client,config)
except ValueError:
    print("Environment variable WORK_CHAT_ID or WAREHOUSE_CHAT_ID is not a valid integer.")
    exit(1)
    
#max_process_time 設為 1200 秒，即 20 分鐘
max_process_time = 1200  # 20分钟
max_media_count = 10  # 10个媒体文件


async def main():
    await client.start(phone_number)
    
    try:
        entity = await client.get_entity('-100'+str(tgbot.config['work_chat_id']))
        tgbot.chat_id = entity.id
    except ValueError as e:
        print(f"Failed to get entity for chat_id {tgbot.config['work_chat_id']}: {e}")
        return

    start_time = time.time()
    media_count = 0
    
    while True:
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
           
            # 跳过来自 WAREHOUSE_CHAT_ID 的对话
            if entity.id == tgbot.config['warehouse_chat_id']:
                continue
           
            # 如果entity.id 是属于 wp_bot 下的 任一 id, 则跳过
            if entity.id in [int(bot['id']) for bot in wp_bot]:
                continue

            if str(entity.id) == '2131062766':
                continue
                
                
           
            # 打印处理的实体名称（频道或群组的标题）
            if isinstance(entity, Channel) or isinstance(entity, Chat):
                entity_title = entity.title
            elif isinstance(entity, User):
                entity_title = f'{entity.first_name or ""} {entity.last_name or ""}'.strip()
            else:
                entity_title = f'Unknown entity {entity.id}'
                
            print(f"\nProcessing entity: {entity.id} - {entity_title}\n")

            if dialog.unread_count >= 0 and (dialog.is_user or dialog.is_group or dialog.is_channel):
                if entity.id == tgbot.config['work_chat_id']:
                    last_read_message_id = 0
                else:
                    last_read_message_id = tgbot.load_last_read_message_id(entity.id)

                print(f">Reading messages from entity {entity.id} - {last_read_message_id}\n")
                async for message in client.iter_messages(entity, min_id=last_read_message_id, limit=30, reverse=True, filter=InputMessagesFilterEmpty()):
                    last_message_id = message.id  # 初始化 last_message_id
                    
                    if message.text:
                        tme_links = re.findall(r'me/\+[a-zA-Z0-9_\-]{15,17}|me/joinchat/[a-zA-Z0-9_\-]{15,18}', message.text)
                        if tme_links:
                            for link in tme_links:
                                if entity.id == tgbot.config['link_chat_id']:
                                    await tgbot.join_channel_from_link(client, "https://t."+link)    
                                else:
                                    await client.send_message(tgbot.config['work_bot_id'], f"https://t.{link}")                 
                        elif entity.id == tgbot.config['work_chat_id']:
                            await tgbot.process_by_check_text(message,'tobot')
                            media_count = media_count + 1
                        elif dialog.is_group or dialog.is_channel:
                           await tgbot.process_by_check_text(message,'encstr')
                    elif message.media:
                        if tgbot.config['warehouse_chat_id']!=0 and entity.id != tgbot.config['work_chat_id'] and entity.id != tgbot.config['warehouse_chat_id']:
                            last_message_id = await tgbot.forward_media_to_warehouse(client,message)
                            media_count = media_count + 1
                    tgbot.save_last_read_message_id(entity.id, last_message_id)
                    
                    if media_count >= max_media_count:
                        break

            elapsed_time = time.time() - start_time
            if elapsed_time > max_process_time:  
                break


            if media_count >= max_media_count:
                print(f"Media count exceeded {max_media_count}. Stopping.\n")
                break

        elapsed_time = time.time() - start_time
        if elapsed_time > max_process_time:  
            print(f"Execution time exceeded {max_process_time} seconds. Stopping.")
            break

        print("Execution time is " + str(elapsed_time) + " seconds. Continuing next cycle... after 80 seconds.")
        await asyncio.sleep(80)  # 间隔80秒

with client:
    client.loop.run_until_complete(main())

from telethon import types
import asyncio
import json
import os


class LYClass:
    def __init__(self, chat_id):
        self.chat_id = chat_id 

    def greet(self, message):
        print(f"Hello, {self.name}!")

    async def wpbot(self, client, message, bot_username):
        try:
            chat_id = self.chat_id
            message_a_id = message.id
            peer_a_id = message.peer_id;
            async with client.conversation(bot_username) as conv:
                # 发送消息到机器人

                forwarded_message = await conv.send_message(message.text)
                
                try:
                    # 获取机器人的响应，等待30秒
                    response = await asyncio.wait_for(conv.get_response(forwarded_message.id), timeout=30)
                    
                except asyncio.TimeoutError:
                    # 如果超时，发送超时消息
                    await client.send_message(chat_id, "the bot was timeout", reply_to=message.id)
                    print("Response timeout.")
                    return


               
              
                if response.media:
                    if isinstance(response.media, types.MessageMediaDocument):
                        mime_type = response.media.document.mime_type
                        if mime_type.startswith('video/'):
                            # 处理视频
                            video = response.media.document
                            await client.send_file(chat_id, video, reply_to=message.id)
                            print("Forwarded video.")
                        else:
                            # 处理文档
                            document = response.media.document
                            await client.send_file(chat_id, document, reply_to=message.id)
                            print("Forwarded document.")
                    elif isinstance(response.media, types.MessageMediaPhoto):
                        # 处理图片
                        photo = response.media.photo
                        await client.send_file(chat_id, photo, reply_to=message.id)
                        print("Forwarded photo.")
                    else:
                        print("Received media, but not a document, video, or photo.")
                elif response.text:
                    # 处理文本
                    

                    # 如果机器人的响应是“在您发的这条消息中，没有代码可以被解析”，则将响应发送到 chat_a_id
                    if response.text == "在您发的这条消息中，没有代码可以被解析":
                        await self.showfiles(client, message)
                    elif response.text == "💔抱歉，未找到可解析内容。":
                        await client.send_message(chat_id, response.text, reply_to=message.id)
                    else:
                        print("Received text response.")


                    
                    

                    
                    

                    print("Forwarded text.")
                else:
                    print("Received non-media and non-text response")



                



        except Exception as e:
            print(f"\rAn error occurred: {e}\n")
    
    async def blgg(self, client, message):
        bot_username = 'FilesDrive_BLGG_bot'
        await self.wpbot(client, message, bot_username)
            
    async def showfiles(self, client, message):
        bot_username = 'ShowFilesBot'
        await self.wpbot(client, message, bot_username)

    async def datapan(self, client, message):
        bot_username = 'datapanbot'
        await self.wpbot(client, message, bot_username)

    async def mediabk(self, client, message):
        bot_username = 'MediaBK2Bot'
        await self.wpbot(client, message, bot_username)

    async def filesave(self, client, message):
        bot_username = 'FileSaveNewBot'
        await self.wpbot(client, message, bot_username)

    async def wangpan(self, client, message):
        bot_username = 'WangPanBOT'
        await self.wpbot(client, message, bot_username)

    async def filetobot(self, client, message):
        bot_username = 'filetobot'
        message.text = "/start "+message.text
        await self.wpbot(client, message, bot_username) 

    async def filein(self, client, message):
        bot_username = 'fileinbot'
        message.text = "/start "+message.text
        await self.wpbot(client, message, bot_username) 

 
    async def fileoffrm(self, client, message):
        bot_username = 'fileoffrm_bot'
        message.text = "/start "+message.text
        await self.wpbot(client, message, bot_username)        


    async def filesave(self, client, message):
        bot_username = 'FileSaveNewBot'
        await self.wpbot(client, message, bot_username)        


 # 机器人信息和正则表达式定义
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
        
# 持久化存储最后读取的消息 ID
LAST_READ_MESSAGE_FILE = "last_read_message_id.json"

def save_last_read_message_id(chat_id, message_id):
    data = {str(chat_id): message_id}
    if os.path.exists(LAST_READ_MESSAGE_FILE):
        with open(LAST_READ_MESSAGE_FILE, 'r') as file:
            existing_data = json.load(file)
        existing_data.update(data)
        data = existing_data

    with open(LAST_READ_MESSAGE_FILE, 'w') as file:
        json.dump(data, file)

def load_last_read_message_id(chat_id):
    if os.path.exists(LAST_READ_MESSAGE_FILE):
        with open(LAST_READ_MESSAGE_FILE, 'r') as file:
            data = json.load(file)
            return data.get(str(chat_id), 0)  # 返回 0 作为默认值
    return 0
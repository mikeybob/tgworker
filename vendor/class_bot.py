from telethon import types
import asyncio
import json
import os


class LYClass:
    def __init__(self, chat_id):
        self.chat_id = chat_id 

    def greet(self, message):
        print(f"Hello, {self.name}!")

    async def send_video_to_filetobot_and_beachboy807bot(self, client, video, original_message):
        chat_id = self.chat_id
        original_message_id = original_message.id

        # 将视频发送到 filetobot 并等待响应
        async with client.conversation('filetobot') as filetobot_conv:
            filetobot_message = await filetobot_conv.send_file(video)
            try:
                # 持续监听
                # ，直到接收到媒体文件
                while True:
                    filetobot_response = await asyncio.wait_for(filetobot_conv.get_response(filetobot_message.id), timeout=30)
                    if filetobot_response.media:
                        # print(f"Received media response: {filetobot_response}\n")
                        # print(f"Received media response: {filetobot_response.message}\n")
                        # print(f"Received media response: {filetobot_response.text}\n")
                        break
                    else:
                        print("Received text response, waiting for media...")

            except asyncio.TimeoutError:
                await client.send_message(chat_id, "filetobot timeout", reply_to=original_message_id)
                print("filetobot response timeout.")
                return

            # 将 filetobot 的响应内容传送给 beachboy807bot，并设置 caption 为原始消息的文本
            async with client.conversation('beachboy807bot') as beachboy807bot_conv:
                caption_text = "|_SendToBeach_|\n"+original_message.text+"\n"+filetobot_response.message
                await beachboy807bot_conv.send_file(filetobot_response.media, caption=caption_text)
                print("Forwarded filetobot response to beachboy807bot with caption.")

                



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
                            
                            # 调用新的函数
                            await self.send_video_to_filetobot_and_beachboy807bot(client, video, message)
                  
                        else:
                            # 处理文档
                            document = response.media.document
                            await client.send_file(chat_id, document, reply_to=message.id)

                            caption_text = "|_SendToBeach_|\n"+message.text
                            await client.send_file("beachboy807bot", document, caption=caption_text)
                            


                            print("Forwarded document.")
                    elif isinstance(response.media, types.MessageMediaPhoto):
                        # 处理图片
                        photo = response.media.photo
                        await client.send_file(chat_id, photo, reply_to=message.id)

                        caption_text = "|_SendToBeach_|\n"+message.text
                        await client.send_file("beachboy807bot", photo, caption=caption_text)
                        
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
                    elif response.text == "此机器人面向外国用户使用，访问 @MediaBKHome 获取面向国内用户使用的机器人":
                        await self.showfiles(client, message)
                    elif response.text == "access @MediaBKHome to get media backup bot for non-chinese-speaking user":
                        await self.mediabk2(client, message)    



                    else:
                        print("Received text response: "+response.text)

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

    async def mediabk2(self, client, message):
        bot_username = 'MediaBKBK1Bot'
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

    async def filespan1(self, client, message):
        bot_username = 'FilesPan1Bot'
        await self.wpbot(client, message, bot_username)  



        
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
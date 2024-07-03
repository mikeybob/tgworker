from telethon import types
import asyncio

class LYClass:
    def __init__(self, name):
        self.name = name

    def greet(self, message):
        print(f"Hello, {self.name}!")

    async def wpbot(self, client, message, bot_username):
        try:
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
                    await client.send_message(-1001717350482, "the bot was timeout", reply_to=message.id)
                    print("Response timeout.")
                    return


               
              
                if response.media:
                    if isinstance(response.media, types.MessageMediaDocument):
                        mime_type = response.media.document.mime_type
                        if mime_type.startswith('video/'):
                            # 处理视频
                            video = response.media.document
                            await client.send_file(-1001717350482, video, reply_to=message.id)
                            print("Forwarded video.")
                        else:
                            # 处理文档
                            document = response.media.document
                            await client.send_file(-1001717350482, document, reply_to=message.id)
                            print("Forwarded document.")
                    elif isinstance(response.media, types.MessageMediaPhoto):
                        # 处理图片
                        photo = response.media.photo
                        await client.send_file(-1001717350482, photo, reply_to=message.id)
                        print("Forwarded photo.")
                    else:
                        print("Received media, but not a document, video, or photo.")
                elif response.text:
                    # 处理文本
                    

                    # 如果机器人的响应是“在您发的这条消息中，没有代码可以被解析”，则将响应发送到 chat_a_id
                    if response.text == "在您发的这条消息中，没有代码可以被解析":
                        await self.showfiles(client, message)
                    elif response.text == "💔抱歉，未找到可解析内容。":
                        await client.send_message(-1001717350482, response.text, reply_to=message.id)
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

 
        
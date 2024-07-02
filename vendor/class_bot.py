class LYClass:
    def __init__(self, name):
        self.name = name

    def greet(self, message):
        print(f"Hello, {self.name}!")

    async def datapan(self, client, message):
        try:
            # 将 message.message 转发给 @datapanbot 机器人
            bot_username = 'datapanbot'
            print(f"Sending message to {bot_username}...")
            sent_message = await client.send_message('datapanbot', 'V_DataPanBot_KAkpwpuqF9D6uT56gExZfqc9e1WYV1CiY7M83qpSRZe94drUxmI0oKNXTG')
            print(f"Sent message to {bot_username}: {sent_message}")

            # 等待机器人的回复
            @client.on(events.NewMessage(from_users=bot_username))
            async def handler(event):
                print(f"Received reply from {bot_username}: {event.message.text}")
                # 停止监听事件
                client.remove_event_handler(handler)
        except Exception as e:
            print(f"An error occurred: {e}")
      


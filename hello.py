from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import InputPeerUser
import os

# 检查是否在本地开发环境中运行
if not os.getenv('GITHUB_ACTIONS'):
    from dotenv import load_dotenv
    load_dotenv()

# 从环境变量中获取值
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
session_name = 'mysession_name'  # 确保与上传的会话文件名匹配

# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient(session_name, api_id, api_hash) as client:
    client.start(phone_number)
     # Send a message
    client.send_message('me', 'Hello, World!')
    print('Message sent successfully!')
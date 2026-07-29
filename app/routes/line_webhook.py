from fastapi import APIRouter, Request, HTTPException, Header
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import os
from dotenv import load_dotenv

# 🟢 สั่งโหลดตัวแปรจากไฟล์ .env
load_dotenv()

router = APIRouter(prefix="/api/line", tags=["LINE Webhook"])

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@router.post("/webhook")
async def line_webhook(request: Request, x_line_signature: str = Header(None)):
    if x_line_signature is None:
        raise HTTPException(status_code=400, detail="Missing X-Line-Signature header")

    body = await request.body()
    body_str = body.decode('utf-8')
    
    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        print(f"Error handling webhook: {e}")
        return "OK"
        
    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    line_user_id = event.source.user_id
    reply_text = f"สวัสดีครับ! LINE ID ของคุณคือ:\n{line_user_id}\n\nนำรหัสนี้ไปกรอกผูกบัญชีในแอปกล่องยาได้เลยครับ"
    
    try:
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_text)]
                )
            )
    except Exception as e:
        print(f"Error sending LINE message: {e}")
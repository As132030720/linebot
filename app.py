from flask import Flask, request, abort, send_from_directory
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import tempfile, os
import datetime
import time
import requests
import openai
import traceback

#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
from news import *
#======這裡是呼叫的檔案內容=====

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key設定
openai.api_key = os.getenv('OPENAI_API_KEY')

def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。', '')
    return answer

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if '功能' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '筆電' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '手機' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '餐廳' in msg:
        message = restaurant(event)
        line_bot_api.reply_message(event.reply_token, message)
        
      if re.match('我想知道南港附近美食', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            '瓦城泰國料理\ngoogle評分=4.1\n評論數量=1020\n*輸入店名以獲得位置資訊'))
      if re.match('瓦城泰國料理', message):
        location_message = LocationSendMessage(
            title='瓦城泰國料理',
            address='115台北市南港區忠孝東路七段369號8樓',
            latitude=25.05382134597444,
            longitude=121.60466156931716
        )
        line_bot_api.reply_message(event.reply_token, location_message)
      else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
    elif '列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    elif '新聞' in msg:
        message = get_latest_article()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
    else:
        try:
            GPT_answer = GPT_response(msg)
            print(GPT_answer)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
        except:
            print(traceback.format_exc())
            line_bot_api.reply_message(event.reply_token, TextSendMessage('你所使用的OPENAI API key額度可能已經超過，請於後台Log內確認錯誤訊息'))

# 處理語音訊息
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    # 取得音訊訊息的 ID
    message_id = event.message.id
    # 從 LINE 伺服器下載音訊訊息
    message_content = line_bot_api.get_message_content(message_id)
    # 建立臨時檔案保存音訊
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    # 定義音訊回應訊息
    message = AudioSendMessage(
        original_content_url=request.host_url + 'static/tmp/' + os.path.basename(tempfile_path),
        duration=event.message.duration
    )
    # 回應音訊訊息
    line_bot_api.reply_message(event.reply_token, message)

# 處理貼圖訊息
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    # 回傳相同的貼圖
    message = StickerSendMessage(
        package_id=event.message.package_id,
        sticker_id=event.message.sticker_id
    )
    line_bot_api.reply_message(event.reply_token, message)

# 處理圖片訊息
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 取得圖片訊息的 ID
    message_id = event.message.id
    # 從 LINE 伺服器下載圖片訊息
    message_content = line_bot_api.get_message_content(message_id)
    # 建立臨時檔案保存圖片
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    # 定義圖片回應訊息
    message = ImageSendMessage(
        original_content_url=request.host_url + 'static/tmp/' + os.path.basename(tempfile_path),
        preview_image_url=request.host_url + 'static/tmp/' + os.path.basename(tempfile_path)
    )
    # 回應圖片訊息
    line_bot_api.reply_message(event.reply_token, message)

# 處理影片訊息
@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):
    # 取得影片訊息的 ID
    message_id = event.message.id
    # 從 LINE 伺服器下載影片訊息
    message_content = line_bot_api.get_message_content(message_id)
    # 建立臨時檔案保存影片
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    # 定義影片回應訊息
    message = VideoSendMessage(
        original_content_url=request.host_url + 'static/tmp/' + os.path.basename(tempfile_path),
        preview_image_url=request.host_url + 'static/tmp/' + os.path.basename(tempfile_path)
    )
    # 回應影片訊息
    line_bot_api.reply_message(event.reply_token, message)


# 端點，用於提供靜態文件
@app.route('/static/tmp/<path:filename>')
def download_file(filename):
    return send_from_directory(static_tmp_path, filename)

@handler.add(PostbackEvent)
def handle_postback(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)




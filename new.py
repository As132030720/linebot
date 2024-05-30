#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import re

def test():
    message = TemplateSendMessage(
        alt_text='圖片旋轉木馬',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url="https://mrmad.com.tw/wp-content/uploads/2022/08/iphone-14-lens-vs-iphone-13-lens-difference-comparison-3.jpg",
                    action=URITemplateAction(
                        label="iphone",
                        uri="https://www.apple.com/tw/iphone/"
                    )
                ),
                ImageCarouselColumn(
                    image_url="https://img.ltn.com.tw/Upload/3c/page/2016/07/14/160714-25278-5.jpg",
                    action=URITemplateAction(
                        label="Android",
                        uri="https://www.android.com/intl/zh-TW_tw/phones-tablets/"
                    )
                ),
                ImageCarouselColumn(
                    image_url="https://i.imgur.com/Np7eFyj.jpg",
                    action=URITemplateAction(
                        label="可愛狗狗",
                        uri="http://imgm.cnmo-img.com.cn/appimg/screenpic/big/674/673928.JPG"
                    )
                ),
                ImageCarouselColumn(
                    image_url="https://i.imgur.com/QRIa5Dz.jpg",
                    action=URITemplateAction(
                        label="可愛貓咪",
                        uri="https://m-miya.net/wp-content/uploads/2014/07/0-065-1.min_.jpg"
                    )
                )
            ]
        )
    )
    return message

def restaurant(event):
    message = text = event.message.text
    if re.match('餐廳', message):
        carousel_template_message = TemplateSendMessage(
            alt_text='免費教學影片',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/wpM584d.jpg',
                        title='南港',
                        text=' ',
                        actions=[
                            MessageAction(
                                label='南港美食',
                                text='我想知道南港附近美食'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://www.google.com/maps/search/%E9%A4%90%E5%BB%B3/@25.052646,121.6074928,17z/data=!3m1!4b1?authuser=0'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/W7nI6fg.jpg',
                        title='市政府',
                        text=' ',
                        actions=[
                            MessageAction(
                                label='市政府美食',
                                text='我想知道市政府附近美食'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://www.google.com/maps/search/%E9%A4%90%E5%BB%B3/@25.0412613,121.563957,17z/data=!3m1!4b1?authuser=0'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/W7nI6fg.jpg',
                        title='台北車站',
                        text=' ',
                        actions=[
                            MessageAction(
                                label='台北車站美食',
                                text='我想知道台北車站附近美食'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://www.google.com/maps/search/%E9%A4%90%E5%BB%B3/@25.0486866,121.5148271,16z/data=!3m1!4b1?authuser=0'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/l7rzfIK.jpg',
                        title='板橋',
                        text=' ',
                        actions=[
                            MessageAction(
                                label='板橋車站美食',
                                text='我想知道板橋車站美食'
                            ),
                            URIAction(
                                label='馬上查看',
                                uri='https://www.google.com/maps/search/%E9%A4%90%E5%BB%B3/@25.0133281,121.4605482,16z/data=!3m1!4b1?authuser=0'
                            )
                        ]
                    )
                ]
            )
        )

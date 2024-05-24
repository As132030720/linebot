#這些是LINE官方開放的套件組合透過import來套用這個檔案上
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

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

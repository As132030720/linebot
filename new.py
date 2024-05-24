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
                    image_url="https://www.bing.com/images/search?view=detailV2&ccid=gmecOAGr&id=C1E07CB975343D08F99416A978D6C738B0C1C1ED&thid=OIP.gmecOAGrAH6rpy8QHFoXbAHaE7&mediaurl=https%3a%2f%2fimage-cdn.hypb.st%2fhttps%3a%2f%2fhk.hypebeast.com%2ffiles%2f2017%2f12%2f2017-top-10-android-smartphones-001.jpg%3fq%3d75%26w%3d800%26cbr%3d1%26fit%3dmax&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.82679c3801ab007eaba72f101c5a176c%3frik%3d7cHBsDjH1nipFg%26pid%3dImgRaw%26r%3d0&exph=533&expw=800&q=android%e6%89%8b%e6%a9%9f&simid=608051044956190891&FORM=IRPRST&ck=4EB31B91DFC313D51D2930DCC8ACDB8D&selectedIndex=0&itb=0",
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

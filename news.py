def get_latest_article():
    url = 'https://ccc.technews.tw/'
    response = requests.get(url)
    if response.status_code != 200:
        return "無法存取該網址。"
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        latest_article = soup.find('div', class_='content')
        if latest_article:
            title = latest_article.find('h1', class_='entry-title').text.strip()
            link = latest_article.find('a')['href']
            return f"{title}\n{link}"
        else:
            return "找不到最新文章。"
        
latest_info = get_latest_article()
print(latest_info)

app = Flask(__name__)

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    if text == "3C新聞":
        latest_info = get_latest_article()
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=latest_info)]
                )
            )


if __name__ == "__main__":
    app.run(port=port)
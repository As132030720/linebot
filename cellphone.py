import requests
from bs4 import BeautifulSoup
import sqlite3

def fetch_data_from_jyes():
    url = 'https://www.jyes.com.tw/product.php?com=1&gad_source=1&gclid=Cj0KCQjwmMayBhDuARIsAM9HM8fHVK8A0jrvOI06TqCnRntev64giOz90ic7-KETtbzD1f-G8LWSsKAaApBdEALw_wcB'
    response = requests.get(url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    product_names = soup.find_all('td', class_='sn', attrs={'data-title': '商品名稱 :'})
    product_prices = soup.find_all('td', class_='p-after sm-half', attrs={'data-title': '門市破盤價 :'})

    products = []

    if len(product_names) == len(product_prices):
        for name_tag, price_tag in zip(product_names, product_prices):
            name_link = name_tag.find('a', class_='tag-link')
            name = name_link.text.strip() if name_link else 'N/A'
            price = price_tag.text.strip() if price_tag else 'N/A'
            products.append((name, price, '傑昇通信'))
    else:
        print("商品名稱和價格數量不一致，請檢查網頁結構。")
    
    return products

def fetch_data_from_landtop(limit=449):
    url = 'https://www.landtop.com.tw/brands'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    count = 0
    for product in soup.find_all('div', class_='title mt-2'):
        if count >= limit:
            break
        name_tag = product.find('a').find('h2')
        if name_tag:
            name = name_tag.text.strip()
            price_tag = product.find_next('span', class_='text-red value')
            if price_tag:
                price = price_tag.text.strip()
                products.append((name, price, '地標網通'))
                count += 1
    
    return products

def create_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            store TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def clear_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('DELETE FROM products')
    conn.commit()
    conn.close()

def save_to_db(products):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.executemany('INSERT INTO products (name, price, store) VALUES (?, ?, ?)', products)
    conn.commit()
    conn.close()

def search_product(product_name):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT name, price, store FROM products WHERE name LIKE ?', ('%' + product_name + '%',))
    results = c.fetchall()
    conn.close()
    return results

# 創建資料庫
create_db()

# 清空舊資料
clear_db()

# 爬取傑昇通信資料並存入資料庫
products_jyes = fetch_data_from_jyes()
if products_jyes:
    save_to_db(products_jyes)
else:
    print("沒有從傑昇通信獲取到商品資料。")


# 爬取地標網通資料並存入資料庫，限制為 449 筆
products_landtop = fetch_data_from_landtop(limit=449)
if products_landtop:
    save_to_db(products_landtop)
else:
    print("沒有從地標網通獲取到商品資料。")

# 設計按鈕模板消息    
def create_store_buttons():
    buttons_template = TemplateSendMessage(
        alt_text='商店選單',
        template=ButtonsTemplate(
            title='請選擇商店',
            text='請選擇您想要的商店',
            actions=[
                PostbackTemplateAction(
                    label='傑昇通信',
                    data='action=choose_store&store=傑昇通信'
                ),
                PostbackTemplateAction(
                    label='地標網通',
                    data='action=choose_store&store=地標網通'
                ),
                PostbackTemplateAction(
                    label='皆可',
                    data='action=choose_store&store=皆可'
                )
            ]
        )
    )
    return buttons_template

def create_phone_buttons():
    buttons_template = TemplateSendMessage(
        alt_text='手機選單',
        template=ButtonsTemplate(
            title='請選擇手機系統',
            text='請選擇您想要的手機系統',
            actions=[
                PostbackTemplateAction(
                    label='Android',
                    data='action=choose&system=android'
                ),
                PostbackTemplateAction(
                    label='iOS',
                    data='action=choose&system=ios'
                )
            ]
        )
    )
    return buttons_template

# 處理文字訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global awaiting_custom_query  # 使用全域變數

    if event.message.text == "手機":
        buttons_template = create_store_buttons()
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif awaiting_custom_query:  # 如果等待用戶輸入自定義查詢
        query = event.message.text
        if query == "結束":
            awaiting_custom_query = False
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='搜尋結束。'))
        else:
            send_custom_query_result(event.reply_token, query)

# 處理Postback事件
@handler.add(PostbackEvent)
def handle_postback(event):
    global awaiting_custom_query, selected_store  # 使用全域變數

    data = event.postback.data
    if data.startswith('action=choose_store&store='):
        selected_store = data.split('=')[-1]
        buttons_template = create_phone_buttons()
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif data.startswith('action=choose&system='):
        system = data.split('=')[-1]
        if system == 'android' or system == 'ios':
            send_brand_buttons(event.reply_token, system)
    elif data.startswith('action=choose_brand&brand='):
        brand = data.split('=')[-1]
        if brand == '其他':
            awaiting_custom_query = True  # 設置標記等待用戶輸入自定義查詢
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入您想要搜尋的產品名稱，或輸入"結束"來結束搜尋：\n範例: HTC U12\niPhone 15\nSamsung A55'))
        else:
            send_model_buttons(event.reply_token, brand)
    elif data.startswith('action=choose_model&model='):
        model = data.split('=')[-1]
        if model == '其他':
            awaiting_custom_query = True  # 設置標記等待用戶輸入自定義查詢
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='請輸入您想要搜尋的產品名稱，或輸入"結束"來結束搜尋：\n範例: HTC U12\niPhone 15\nSamsung A55'))
        else:
            send_product_info(event.reply_token, model)

# 設計品牌選單
def send_brand_buttons(reply_token, system):
    if system == 'ios':
        brands = ['Apple']
    else:
        brands = ['SAMSUNG', 'ASUS', 'SONY', '其他']

    actions = [PostbackTemplateAction(label=brand, data=f'action=choose_brand&brand={brand}') for brand in brands]

    buttons_template = TemplateSendMessage(
        alt_text='手機品牌選單',
        template=ButtonsTemplate(
            title=f'請選擇{system.capitalize()}手機品牌',
            text=f'請選擇您想要的{system.capitalize()}手機品牌',
            actions=actions
        )
    )
    line_bot_api.reply_message(reply_token, buttons_template)

# 設計型號選單
def send_model_buttons(reply_token, brand):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    query = "SELECT name FROM products WHERE name LIKE ?"
    params = (f'{brand}%',)

    if selected_store != '皆可':
        query += " AND store = ?"
        params = (f'{brand}%', selected_store)

    c.execute(query, params)
    models = [row[0] for row in c.fetchall()]
    conn.close()

    actions = []
    for model in models[:3]:  # 確保前三個選項
        label = model if len(model) <= 20 else model[:20]  # 確保標籤長度不超過20個字元
        actions.append(PostbackTemplateAction(label=label, data=f'action=choose_model&model={model}'))

    actions.append(PostbackTemplateAction(label='其他', data='action=choose_model&model=其他'))  # 添加“其他”選項

    buttons_template = TemplateSendMessage(
        alt_text='手機型號選單',
        template=ButtonsTemplate(
            title=f'請選擇{brand}手機型號',
            text=f'請選擇您想要的{brand}手機型號',
            actions=actions
        )
    )
    line_bot_api.reply_message(reply_token, buttons_template)

# 查詢並發送自定義產品結果
def send_custom_query_result(reply_token, query):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    sql_query = "SELECT name, price, store FROM products WHERE name LIKE ?"
    params = (f'%{query}%',)

    if selected_store != '皆可':
        sql_query += " AND store = ?"
        params = (f'%{query}%', selected_store)

    c.execute(sql_query, params)
    rows = c.fetchall()
    conn.close()

    if rows:
        messages = [TextSendMessage(text=f'商品名稱: {row[0]}, 價格: {row[1]}, 商店: {row[2]}') for row in rows]
    else:
        messages = [TextSendMessage(text='找不到相關商品')]

    # 確保一次回覆的消息數量不超過 5
    if len(messages) > 4:
        line_bot_api.reply_message(reply_token, messages[:4])
    else:
        line_bot_api.reply_message(reply_token, messages)

    # 提示用戶繼續輸入
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text='請輸入您想要搜尋的產品名稱，或輸入"結束"來結束搜尋：'))

# 從資料庫中檢索商品資訊
def send_product_info(reply_token, model):
    global selected_product_info  # 使用全域變數

    if model in selected_product_info:  # 如果已經暫存了該商品資訊，直接回覆
        product_info = selected_product_info[model]
        line_bot_api.reply_message(reply_token, product_info)
    else:  # 否則從資料庫中查詢並回覆
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        sql_query = 'SELECT name, price, store FROM products WHERE name = ?'
        params = (model,)

        if selected_store != '皆可':
            sql_query += " AND store = ?"
            params = (model, selected_store)

        c.execute(sql_query, params)
        rows = c.fetchall()
        conn.close()

        if rows:
            messages = [TextSendMessage(text=f'商品名稱: {row[0]}, 價格: {row[1]}, 商店: {row[2]}') for row in rows]
            selected_product_info[model] = messages  # 暫存商品資訊
        else:
            messages = [TextSendMessage(text='找不到相關商品')]

        line_bot_api.reply_message(reply_token, messages)

if __name__ == "__main__":
    app.run()
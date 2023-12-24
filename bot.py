import re
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id = '10261086'
api_hash = '9195dc0591fbdb22b5711bcd1f437dab'
bot_token = '6524742034:AAG4zKlNlSHsNnjKZ8Y3rk_eaxBiLQ2X9Hw'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@app.on_message(filters.command("start"))
def random_answer(client, message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("View Movies", callback_data="view")]]
    )
    message.reply_text(
        "Hello👋 \n\n🗳Get latest Movies from 1Tamilmv\n\n⚙️*How to use me??*🤔\n\n✯ Please Enter */view* command and you'll get magnet link as well as a link to the torrent file 😌\n\nShare and Support💝",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=keyboard,
    )


@app.on_message(filters.command("view"))
def start(client, message):
    message.reply_text("Please wait for 10 seconds", parse_mode=enums.ParseMode.HTML)
    tamilmv()
    keyboard = make_keyboard()
    message.reply_text(
        "Select a Movie from the list 🙂 : ", reply_markup=keyboard, parse_mode=enums.ParseMode.HTML
    )


@Client.on_callback_query(filters.callback_query)
async def callback_query_handler(client, callback_query):
    chat_id = callback_query.message.chat.id
    await client.send_message(chat_id, text="Here's your Movie links 🎥 ", parse_mode=enums.ParseMode.HTML)

    for key, value in enumerate(movie_list):
        if callback_query.data == f"{key}":
            print("HI")
            if movie_list[int(callback_query.data)] in real_dict.keys():
                for i in real_dict[movie_list[int(callback_query.data)]]:
                    await client.send_message(chat_id, text=f"{i}\n\n🤖 @Tamilmv_movie_bot", parse_mode=enums.ParseMode.HTML)
                    print(real_dict[movie_list[int(callback_query.data)]])

    await client.send_message(chat_id, text="🌐 Please Join Our Status Channel", parse_mode=enums.ParseMode.HTML, reply_markup=make_keyboard())


def make_keyboard():
    markup = InlineKeyboardMarkup()

    for key, value in enumerate(movie_list):
        markup.add(InlineKeyboardButton(text=value, callback_data=f"{key}"))

    return markup


@app.on_message()
def tamilmv(client, message):
    main_url = 'https://www.1tamilmv.tips/'
    main_link = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection': 'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }

    global movie_dict
    movie_dict = {}
    global real_dict
    real_dict = {}
    web = requests.get(main_url, headers=headers)
    soup = BeautifulSoup(web.text, 'lxml')
    linker = []
    bad_titles = []
    real_titles = []
    global movie_list
    movie_list = []

    num = 0

    temps = soup.find_all('div', {'class': 'ipsType_break ipsContained'})

    for i in range(21):
        title = temps[i].findAll('a')[0].text
        bad_titles.append(title)
        links = temps[i].find('a')['href']
        content = str(links)
        linker.append(content)

    for element in bad_titles:
        real_titles.append(element.strip())
        movie_dict[element.strip()] = None
    print(bad_titles)
    movie_list = list(movie_dict)

    for url in linker:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        pattern = re.compile(r"magnet:\?xt=urn:[a-z0-9]+:[a-zA-Z0-9]{40}")
        big_title = soup.find_all('a')
        all_titles = []
        file_link = []
        mag = []
        for i in soup.find_all('a', href=True):
            if i['href'].startswith('magnet'):
                mag.append(i['href'])

        for a in soup.findAll('a', {"data-fileext": "torrent", 'href': True}):
            file_link.append(a['href'])

        for title in big_title:
            if title.find('span') is None:
                pass
            else:
                if title.find('span').text.endswith('torrent'):
                    all_titles.append(title.find('span').text[19:-8])

        for p in range(0, len(mag)):
            try:
                real_dict.setdefault(movie_list[num], [])
                real_dict[movie_list[num]].append(
                    (f"*{all_titles[p]}* -->\n🧲 `{mag[p]}`\n🗒️->[Torrent file]({file_link[p]})"))
            except:
                pass

        num = num + 1


if __name__ == "__main__":
    app.run()

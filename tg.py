import time
import telebot
from telebot import types
import script

# Ініціалізація бота
bot_token = '6183264828:AAGSD5Pi1kKZbPvi--qJDuYZi3M8PcK8o_Q'
bot = telebot.TeleBot(bot_token)
tg_chat_id = '@yegvbkslfnhk'


def send_notification(car):
    title = car['title']
    price = car['price']
    mileage = car['mileage']
    location = car['location']
    photos, vin = script.scrape_images(car['link'])
    media_list = []

    message = f"<b><a href='{car['link']}'>{title}</a></b>\n" \
              f"Ціна: \U0001F4B5 {price.replace(' ', '')} $\n" \
              f"Пробіг: \U0001F697{mileage}\n" \
              f"Місто: \U0001F30D{location.replace('( від )', '')}\n" \
              f"🇺🇸 <b><a href='{vin}'>Bidfax</a></b>"

    for photo in photos:
        media = types.InputMediaPhoto(media=photo, caption=message if photos.index(photo) == 0 else '', parse_mode='HTML')
        media_list.append(media)
    if vin != '' and vin != 'https://auto.ria.com/uk':
        usa_photos = script.scrape_usa_images(vin)
        if usa_photos:
            media_usa = [types.InputMediaPhoto(media=photo_us) for photo_us in usa_photos]
            bot.send_media_group(tg_chat_id, media_list, disable_notification=True, timeout=30)
            bot.send_media_group(tg_chat_id, media_usa, disable_notification=True, timeout=30)
            time.sleep(60)
        else:
            bot.send_media_group(tg_chat_id, media_list, disable_notification=True, timeout=30)
            time.sleep(30)
    else:
        bot.send_media_group(tg_chat_id, media_list, disable_notification=True, timeout=30)
        time.sleep(30)


def send_price_change_notification(car_title, current_price, car_link):
    photos, vin = script.scrape_images(car_link)
    media_list = []
    message = f"<b><a href='{car_link}'>{car_title}</a></b>\n" \
              f"Нова ціна: \U0001F4B5 {current_price.replace(' ', '')} $\n"
    for photo in photos:
        media = types.InputMediaPhoto(media=photo, caption=message if photos.index(photo) == 0 else '',
                                      parse_mode='HTML')
        media_list.append(media)
    time.sleep(20)
    bot.send_media_group(tg_chat_id, media_list, disable_notification=True, timeout=30)


def send_car_sold_notification(car_id, title, link):
    photos, vin = script.scrape_images(link)
    media_list = []
    message = f"<b><a href='{link}'>{title}</a></b>\n" \
              f"Автомобіль проданий!\nID: {car_id}"
    for photo in photos:
        media = types.InputMediaPhoto(media=photo, caption=message if photos.index(photo) == 0 else '',
                                      parse_mode='HTML')
        media_list.append(media)
    time.sleep(20)
    bot.send_media_group(tg_chat_id, media_list, disable_notification=True, timeout=30)

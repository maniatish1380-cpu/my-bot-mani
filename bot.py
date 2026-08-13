import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import json
import os
from datetime import datetime

TOKEN = '8873507987:AAGgl-3ieIbEnYWblGAnjHxerKii5kxs_E0'
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'users.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🎁 اکانت روزانه 🎁"), 
        KeyboardButton("🎁 اکانت ۱۵ میتیک رایگان 🎁"),
        KeyboardButton("📊 لینک دعوت (رفرال)"),
        KeyboardButton("🌐 DNS اختصاصی رایگان"),
        KeyboardButton("📢 کانال تلگرام"),
        KeyboardButton("📸 پیج اینستاگرام")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    args = message.text.split()
    data = load_data()
    
    if user_id not in data:
        data[user_id] = {'invites': 0, 'last_daily': None}
        if len(args) > 1:
            inviter_id = args[1]
            if inviter_id != user_id and inviter_id in data:
                data[inviter_id]['invites'] += 1
        save_data(data)
        
    bot.send_message(message.chat.id, "سلام! به ربات خوش آمدید:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = str(message.from_user.id)
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")

    if user_id not in data:
        data[user_id] = {'invites': 0, 'last_daily': None}

    if message.text == "🎁 اکانت روزانه 🎁":
        if data[user_id].get('last_daily') == today:
            bot.send_message(message.chat.id, "❌ شما امروز اکانت روزانه را دریافت کردید. فردا دوباره تلاش کنید.")
        else:
            msg = "🎁 این هم اکانت روزانه شما:\n\nsajad.calaf031@gmail.com\nSAJAD1401"
            bot.send_message(message.chat.id, msg)
            data[user_id]['last_daily'] = today
            save_data(data)

    elif message.text == "🎁 اکانت ۱۵ میتیک رایگان 🎁":
        current_invites = data[user_id].get('invites', 0)
        
        if current_invites >= 5:
            prize_msg = "💎 تبریک! شما ۵ نفر را دعوت کردید و اکانت ۱۵ میتیک برای شما آزاد شد:\n\njosueljesus769@gmail.com\nAjj,9120"
            bot.send_message(message.chat.id, prize_msg)
        else:
            remaining = 5 - current_invites
            ref_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
            
            ref_msg = (
                f"⚠️ شما هنوز ۵ نفر را دعوت نکرده‌اید!\n\n"
                f"👥 تعداد دعوت‌های فعلی شما: {current_invites} نفر\n"
                f"❌ تعداد باقی‌مانده برای دریافت میتیک: {remaining} نفر\n\n"
                f"🔗 برای دریافت اکانت ۱۵ میتیک، لینک زیر را برای دوستان خود بفرستید:\n{ref_link}"
            )
            bot.send_message(message.chat.id, ref_msg)

    elif message.text == "📊 لینک دعوت (رفرال)":
        current_invites = data[user_id].get('invites', 0)
        ref_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
        bot.send_message(message.chat.id, f"📊 وضعیت دعوت‌های شما: {current_invites} نفر\n\n🔗 لینک اختصاصی شما:\n{ref_link}")

    elif message.text == "🌐 DNS اختصاصی رایگان":
        dns_msg = ("🌐 **DNS اختصاصی و پرسرعت رایگان:**\n\nPrimary DNS: `77.88.8.8`\nSecondary DNS: `88.198.220.33`")
        bot.send_message(message.chat.id, dns_msg, parse_mode="Markdown")

    elif message.text == "📢 کانال تلگرام":
        bot.send_message(message.chat.id, "📢 کانال ما:\nhttps://t.me/cod_manii_yt")

    elif message.text == "📸 پیج اینستاگرام":
        bot.send_message(message.chat.id, "📸 پیج اینستاگرام ما:\nhttps://www.instagram.com/maniiii.yt?igsh=ZWp6ZHdhMjloY2Jh")

print("Bot with Mythic account is running...")
bot.infinity_polling()


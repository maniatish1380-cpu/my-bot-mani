import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
from datetime import datetime

TOKEN = '8873507987:AAGgl-3ieIbEnYWblGAnjHxerKii5kxs_E0'
ADMIN_ID = 6903327854
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'users.json'
CHANNEL_USERNAME = '@cod_manii_yt'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception:
        pass
    return False

def not_joined_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 عضويت در کانال تلگرام", url=f"https://t.me/cod_manii_yt"))
    markup.add(InlineKeyboardButton("🔄 بررسی عضویت", callback_data="check_join"))
    return markup

def main_menu(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🎁 اکانت روزانه 🎁"), 
        KeyboardButton("🎁 اکانت ۲۱ میتیک رایگان 🎁"),
        KeyboardButton("🎁 پست سایرن رایگان"),
        KeyboardButton("🎁  پست اکانت ۸۰ میلیونی رایگان🎁"),
        KeyboardButton("🎁 ردیم کد کالاف"),
        KeyboardButton("📊 لینک دعوت (رفرال)"),
        KeyboardButton("🌐 DNS اختصاصی رایگان"),
        KeyboardButton("📢 کانال تلگرام"),
        KeyboardButton("📸 پیج اینستاگرام"),
        KeyboardButton("🔄 بروزرسانی منو")
    )
    if user_id == ADMIN_ID:
        markup.add(KeyboardButton("📊 اطلاعات و آمار ربات (ادمین)"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    numeric_user_id = message.from_user.id
    
    if not check_membership(numeric_user_id):
        bot.send_message(message.chat.id, "⚠️ برای استفاده از ربات، ابتدا باید در کانال ما عضو شوید!", reply_markup=not_joined_markup())
        return

    args = message.text.split()
    data = load_data()
    
    if user_id not in data:
        data[user_id] = {'invites': 0, 'last_daily': None}
        if len(args) > 1:
            inviter_id = args[1]
            if inviter_id != user_id and inviter_id in data:
                data[inviter_id]['invites'] += 1
        save_data(data)
        
    bot.send_message(message.chat.id, "سلام! به ربات خوش آمدید:", reply_markup=main_menu(numeric_user_id))

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_check_join(call):
    if check_membership(call.from_user.id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ عضویت تایید شد!", reply_markup=main_menu(call.from_user.id))
    else:
        bot.answer_callback_query(call.id, "❌ هنوز عضو نشدید!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = str(message.from_user.id)
    if not check_membership(message.from_user.id):
        bot.send_message(message.chat.id, "⚠️ ابتدا در کانال عضو شوید!", reply_markup=not_joined_markup())
        return

    data = load_data()
    if user_id not in data: data[user_id] = {'invites': 0, 'last_daily': None}
    
    today = datetime.now().strftime("%Y-%m-%d")
    current_invites = data[user_id].get('invites', 0)

    if message.text == "🎁 اکانت ۸۰ میلیونی رایگان🎁":
        bot.send_message(message.chat.id, "🎁 اطلاعات اکانت ۸۰ میلیونی:\nimamirnazari@gmail.com\nmeysam2020")

    elif message.text == "🎁 ردیم کد کالاف":
        if current_invites >= 1:
            codes = ("DCEPZBZKFD\nDCCKZBZNB5\nDCCJZBZN4J\nDCCHZBZR3K\nDCCGZBZNCX\nDBGOZBZD8M\nDAVAZBZ9EP\nDAVCZBZA9M\nDAVBZBZX5A\nDBDKZBZQUU\nDBDJZBZAJU\nDAVGZBZRN6\nDBVPZBZNDX\nDBVHZBZUF3\nDBVNZBZBQW\nWELOVEMOM\nDCUPZBZ84M\nCTULZBZBXP\nCTJQZBZAFS\nCTJNZBZKJ8\nCUAMZBZFCF\n\n"
                     "نکته: اگر موقع زدن بعضی از این کدها ارور داد، یعنی ظرفیت آن کد پر شده یا منقضی شده است؛ چون کدهای اینستاگرام و بازی‌ها ظرفیت محدودی دارند. اول کدهای بالای لیست را تست کنید.")
            bot.send_message(message.chat.id, codes)
        else:
            bot.send_message(message.chat.id, f"⚠️ برای دریافت ردیم کد، باید حداقل ۱ نفر را دعوت کرده باشید.\nتعداد دعوت فعلی شما: {current_invites}\nلینک دعوت: https://t.me/{(bot.get_me()).username}?start={user_id}")
    
    # سایر بخش‌ها (اکانت روزانه، ۲۱ میتیک و غیره) بدون تغییر باقی ماندند...
    elif message.text == "🔄 بروزرسانی منو":
        bot.send_message(message.chat.id, "✅ منو بروزرسانی شد.", reply_markup=main_menu(message.from_user.id))
    
    # ... (کدهای قبلی خود را در اینجا قرار دهید)

bot.infinity_polling()

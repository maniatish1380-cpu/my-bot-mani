import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
from datetime import datetime

TOKEN = '8873507987:AAGgl-3ieIbEnYWblGAnjHxerKii5kxs_E0'
bot = telebot.TeleBot(TOKEN)

# آیدی عددی شما به عنوان ادمین ربات
ADMIN_ID = 6903327854

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
        KeyboardButton("🎁 اکانت ۱۵ میتیک رایگان 🎁"),
        KeyboardButton("📊 لینک دعوت (رفرال)"),
        KeyboardButton("🌐 DNS اختصاصی رایگان"),
        KeyboardButton("📢 کانال تلگرام"),
        KeyboardButton("📸 پیج اینستاگرام")
    )
    # اگر واردکننده دستور، خودِ تو بودی دکمه آمار اضافه میشه
    if str(user_id) == str(ADMIN_ID):
        markup.add(KeyboardButton("📊 آمار کاربران"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if not check_membership(message.from_user.id):
        bot.send_message(message.chat.id, "⚠️ برای استفاده از ربات، ابتدا باید در کانال ما عضو شوید:", reply_markup=not_joined_markup())
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
    bot.send_message(message.chat.id, "سلام! به ربات خوش آمدید:", reply_markup=main_menu(user_id))

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_check_join(call):
    user_id = call.from_user.id
    if check_membership(user_id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "✅ تایید شد! به ربات خوش آمدید:", reply_markup=main_menu(user_id))
    else:
        bot.answer_callback_query(call.id, "❌ شما هنوز در کانال عضو نشده‌اید!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = str(message.from_user.id)
    if not check_membership(message.from_user.id):
        bot.send_message(message.chat.id, "⚠️ برای استفاده از ربات، ابتدا باید در کانال ما عضو شوید!", reply_markup=not_joined_markup())
        return

    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")

    if user_id not in data:
        data[user_id] = {'invites': 0, 'last_daily': None}

    if message.text == "🎁 اکانت روزانه 🎁":
        if data[user_id].get('last_daily') == today:
            bot.send_message(message.chat.id, "❌ شما امروز اکانت روزانه را دریافت کردید. فردا دوباره تلاش کنید.")
        else:
            bot.send_message(message.chat.id, "🎁 این هم اکانت روزانه شما:\n\nsajad.calaf031@gmail.com\nSAJAD1401")
            data[user_id]['last_daily'] = today
            save_data(data)

    elif message.text == "🎁 اکانت ۱۵ میتیک رایگان 🎁":
        current_invites = data[user_id].get('invites', 0)
        if current_invites >= 5:
            bot.send_message(message.chat.id, "💎 تبریک! شما ۵ نفر را دعوت کردید و اکانت ۱۵ میتیک برای شما آزاد شد:\n\njosueljesus769@gmail.com\nAjj,9120")
        else:
            remaining = 5 - current_invites
            ref_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
            bot.send_message(message.chat.id, f"⚠️ شما هنوز ۵ نفر را دعوت نکرده‌اید!\n\n👥 تعداد دعوت‌های فعلی: {current_invites} نفر\n❌ باقی‌مانده: {remaining} نفر\n\n🔗 لینک دعوت شما:\n{ref_link}")

    elif message.text == "📊 آمار کاربران" and str(user_id) == str(ADMIN_ID):
        total_users = len(data)
        active_invites_sum = sum(user_info.get('invites', 0) for user_info in data.values())
        stats_msg = (
            f"📊 **آمار کلی ربات:**\n\n"
            f"👥 کل کاربران ربات: {total_users} نفر\n"
            f"🔗 مجموع دعوت‌های ثبت‌شده: {active_invites_sum}"
        )
        bot.send_message(message.chat.id, stats_msg, parse_mode="Markdown")

    elif message.text == "📊 لینک دعوت (رفرال)":
        current_invites = data[user_id].get('invites', 0)
        ref_link = f"https://t.me/{(bot.get_me()).username}?start={user_id}"
        bot.send_message(message.chat.id, f"📊 وضعیت دعوت‌های شما: {current_invites} نفر\n\n🔗 لینک اختصاصی شما:\n{ref_link}")

    elif message.text == "🌐 DNS اختصاصی رایگان":
        bot.send_message(message.chat.id, "🌐 DNS اختصاصی و پرسرعت رایگان:\n\nPrimary DNS: 77.88.8.8\nSecondary DNS: 88.198.220.33", parse_mode="Markdown")

    elif message.text == "📢 کانال تلگرام":
        bot.send_message(message.chat.id, "📢 کانال ما:\nhttps://t.me/cod_manii_yt")

    elif message.text == "📸 پیج اینستاگرام":
        bot.send_message(message.chat.id, "📸 پیج اینستاگرام ما:\nhttps://www.instagram.com/maniiii.yt?igsh=ZWp6ZHdhMjloY2Jh")

print("Bot with Mythic account and Forced Join is running...")
bot.infinity_polling()


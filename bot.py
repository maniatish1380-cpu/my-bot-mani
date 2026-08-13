import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
from datetime import datetime

TOKEN = '8873507987:AAGgl-3ieIbEnYWblGAnjHxerKii5kxs_E0'
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'users.json'
CHANNEL_USERNAME = '@cod_manii_yt'  # آیدی کانال شما برای جوین اجباری

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# تابع بررسی عضویت کاربر در کانال
def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception:
        pass
    return False

# دکمه‌های عضویت در کانال (شیشه ای)
def not_joined_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 عضويت در کانال تلگرام", url=f"https://t.me/cod_manii_yt"))
    markup.add(InlineKeyboardButton("🔄 بررسی عضویت", callback_data="check_join"))
    return markup

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
    
    # اول چک می‌کنیم عضو کانال هست یا نه
    if not check_membership(message.from_user.id):
        bot.send_message(
            message.chat.id, 
            "⚠️ برای استفاده از ربات، ابتدا باید در کانال ما عضو شوید!\n\nپس از عضویت، روی دکمه‌ی «بررسی عضویت» بزنید:", 
            reply_markup=not_joined_markup()
        )
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
        
    bot.send_message(message.chat.id, "سلام! به ربات خوش آمدید:", reply_markup=main_menu())

# هندلر برای دکمه شیشه ای بررسی عضویت
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def callback_check_join(call):
    user_id = call.from_user.id
    if check_membership(user_id):
        bot.answer_callback_query(call.id, "✅ تایید شد! حالا می‌تونید از ربات استفاده کنید.")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "سلام! به ربات خوش آمدید:", reply_markup=main_menu())
    else:
        bot.answer_callback_query(call.id, "❌ شما هنوز در کانال عضو نشده‌اید!", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = str(message.from_user.id)
    
    # چک کردن جوین اجباری برای تمام پیام‌ها و دکمه‌ها
    if not check_membership(message.from_user.id):
        bot.send_message(
            message.chat.id, 
            "⚠️ برای استفاده از ربات، ابتدا باید در کانال ما عضو شوید!", 
            reply_markup=not_joined_markup()
        )
        return

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

print("Bot with Mythic account and Forced Join is running...")
bot.infinity_polling()

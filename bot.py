import os
import telebot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
import json

# ==================== تنظیمات ربات ====================
API_TOKEN = '8873507987:AAG3xEQ1fF8SQHjdfY2HQxA5wuYDRKltlPs'  # توکن جدید شما
bot = telebot.TeleBot(API_TOKEN)

# آیدی ادمین و کانال اجباری
ADMIN_ID = 6903327854
CHANNEL_USERNAME = '@TRUST1_MANI'  # یوزرنیم کانال شما

# تعداد رفرال مورد نیاز برای گرفتن جایزه 20 فول
REQUIRED_REFS_FOR_20_FULL = 45

# متن جایزه 20 فول
REWARD_20_FULL_PRIZE = (
    '🎁 تبریک! شما به تعداد رفرال مقرر (۴۵ نفر) رسیدید.\nلینک جایزه'
    ' ۲۰ فول شما:\nhttps://t.me/TRUST1_MANI/28'
)

# فایل ذخیره اطلاعات کاربران
DATA_FILE = 'users.json'


def load_data():
  if not os.path.exists(DATA_FILE):
    return {}
  try:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
      return json.load(f)
  except:
    return {}


def save_data(data):
  with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# بررسی عضویت کاربر در کانال
def check_membership(user_id):
  try:
    status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
    return status in ['member', 'administrator', 'creator']
  except Exception as e:
    print(f'Error checking membership: {e}')
    return True


# دکمه‌های شیشه‌ای برای عضویت اجباری
def not_joined_markup():
  markup = InlineKeyboardMarkup()
  markup.add(
      InlineKeyboardButton(
          '📢 عضويت در كانال', url=f'https://t.me/{CHANNEL_USERNAME[1:]}'
      )
  )
  markup.add(
      InlineKeyboardButton('🔄 عضو شدم، بررسی مجدد', callback_data='check_join')
  )
  return markup


# کیبورد اصلی ربات
def main_menu():
  markup = ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add(KeyboardButton('🎁 فول رایگان 40 👤'))
  markup.add(KeyboardButton('🎁 اکانت 20 فول رایگان'))
  markup.add(KeyboardButton('👥 لینک دعوت (رفرال)'))
  markup.add(KeyboardButton('📢 کانال تلگرام'), KeyboardButton('📸 پیج اینستاگرام'))
  return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_id = str(message.from_user.id)
  args = message.text.split()

  data = load_data()

  # ثبت‌نام کاربر جدید
  if user_id not in data:
    data[user_id] = {'invited_count': 0, 'invited_by': None, 'claimed_20_full': False}

    # بررسی سیستم رفرال
    if len(args) > 1:
      inviter_id = args[1]
      if inviter_id != user_id and inviter_id in data:
        data[user_id]['invited_by'] = inviter_id
        data[inviter_id]['invited_count'] += 1

        # ارسال پیام به معرف
        try:
          bot.send_message(
              inviter_id,
              f'🎉 یک نفر با لینک دعوت شما وارد ربات شد!\nتعداد رفرال‌های شما:'
              f' {data[inviter_id]["invited_count"]}',
          )

          if (
              data[inviter_id]['invited_count'] >= REQUIRED_REFS_FOR_20_FULL
              and not data[inviter_id]['claimed_20_full']
          ):
            data[inviter_id]['claimed_20_full'] = True
            bot.send_message(
                inviter_id,
                f'🏆 تبریک! شما به {REQUIRED_REFS_FOR_20_FULL} رفرال رسیدید و'
                f' جایزه خود را دریافت کردید:\n\n{REWARD_20_FULL_PRIZE}',
            )
        except Exception as e:
          print(f'Could not notify inviter {inviter_id}: {e}')

    save_data(data)

  if not check_membership(int(user_id)):
    try:
      bot.send_message(
          message.chat.id,
          '⚠️ برای استفاده از ربات، ابتدا باید در کانال ما عضو شوید 👇',
          reply_markup=not_joined_markup(),
      )
    except Exception as e:
      print(f'Error: {e}')
    return

  try:
    bot.send_message(
        message.chat.id,
        'سلام! به ربات خوش آمدید. از منوی زیر یکی از گزینه‌ها را انتخاب کنید:',
        reply_markup=main_menu(),
    )
  except Exception as e:
    print(f'Error: {e}')


@bot.callback_query_handler(func=lambda call: call.data == 'check_join')
def callback_check_join(call):
  user_id = str(call.from_user.id)
  if check_membership(int(user_id)):
    bot.answer_callback_query(call.id, '✅ عضویت شما تایید شد!')
    bot.send_message(
        call.message.chat.id,
        'ممنون از عضویت شما! منوی ربات بروز شد.',
        reply_markup=main_menu(),
    )
  else:
    bot.answer_callback_query(
        call.id, '❌ شما هنوز در کانال عضو نشده‌اید!', show_alert=True
    )


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
  user_id = str(message.from_user.id)

  if not check_membership(int(user_id)):
    bot.send_message(
        message.chat.id,
        '⚠️ برای استفاده از ربات، ابتدا باید در کانال ما عضو شوید 👇',
        reply_markup=not_joined_markup(),
    )
    return

  text = message.text
  data = load_data()
  if user_id not in data:
    data[user_id] = {'invited_count': 0, 'invited_by': None, 'claimed_20_full': False}
    save_data(data)

  if text == '📢 کانال تلگرام':
    bot.send_message(
        message.chat.id, f'📢 کانال ما: https://t.me/{CHANNEL_USERNAME[1:]}'
    )
  elif text == '📸 پیج اینستاگرام':
    bot.send_message(
        message.chat.id, '📸 پیج اینستاگرام ما: https://instagram.com/maniiii.yt'
    )
  elif text == '👥 لینک دعوت (رفرال)':
    bot_info = bot.get_me()
    ref_link = f'https://t.me/{bot_info.username}?start={user_id}'
    count = data[user_id].get('invited_count', 0)
    bot.send_message(
        message.chat.id,
        f'🔗 با ارسال لینک زیر به دوستانتان، می‌توانید آنها را دعوت کنید:\n\n`{ref_link}`\n\n👥'
        f' تعداد افرادی که تا الان دعوت کردید: **{count} نفر**\n🎁 برای دریافت'
        f' بخش **اکانت ۲۰ فول رایگان** به **{REQUIRED_REFS_FOR_20_FULL} نفر**'
        ' رفرال نیاز داری.',
        parse_mode='Markdown',
    )
  elif 'فول رایگان 40' in text:
    markup_post = InlineKeyboardMarkup()
    markup_post.add(
        InlineKeyboardButton(
            '🔗 ورود به پست ۴۰ فول رایگان',
            url='https://t.me/TRUST1_MANI/28',
        )
    )
    bot.send_message(
        message.chat.id,
        '🎁 **بخش فول رایگان ۴۰:**\n\nبرای دریافت و مشاهده پست مربوطه، روی'
        ' دکمه زیر کلیک کنید:',
        reply_markup=markup_post,
    )
  elif text == '🎁 اکانت 20 فول رایگان':
    count = data[user_id].get('invited_count', 0)
    already_claimed = data[user_id].get('claimed_20_full', False)

    if already_claimed:
      bot.send_message(
          message.chat.id,
          '❌ شما قبلاً جایزه این بخش را دریافت کرده‌اید!',
          reply_markup=main_menu(),
      )
    elif count >= REQUIRED_REFS_FOR_20_FULL:
      data[user_id]['claimed_20_full'] = True
      save_data(data)
      bot.send_message(
          message.chat.id, REWARD_20_FULL_PRIZE, reply_markup=main_menu()
      )
    else:
      needed = REQUIRED_REFS_FOR_20_FULL - count
      bot.send_message(
          message.chat.id,
          f'❌ شرایط دریافت اکانت ۲۰ فول رایگان تکمیل نشده است!!\n📌 تعداد رفرال'
          f' مورد نیاز: **{REQUIRED_REFS_FOR_20_FULL} نفر**\n⚠️ تعداد فعلی شما:'
          f' **{count} نفر**\n\n⏳ شما باید **{needed} نفر دیگر** دعوت کنی تا'
          ' این جایزه آزاد شود.',
          reply_markup=main_menu(),
          parse_mode='Markdown',
      )


if __name__ == '__main__':
  bot.infinity_polling()

"""
SM Quality — Telegram Bot
مع Flask Keep-Alive للاستضافة المجانية على Render
"""

import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os

# ══════════════════════════════════════
#  إعدادات البوت — لا تضع التوكن هنا
#  ضعه في متغيرات البيئة على Render
# ══════════════════════════════════════
BOT_TOKEN      = os.environ.get("8634912764:AAFHRGDml2jK-sABMkhLWEV9Ax-HIPdDYTg")
ADMIN_CHAT_ID  = int(os.environ.get("ADMIN_CHAT_ID", "6978577379"))

INSTAGRAM_USERNAME = "sm___quality"
INSTAGRAM_URL      = f"https://www.instagram.com/{INSTAGRAM_USERNAME}/"

# ══════════════════════════════════════
#  Flask — Keep Alive
# ══════════════════════════════════════
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ SM Quality Bot is alive!", 200

@app.route("/health")
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ══════════════════════════════════════
#  إنشاء البوت
# ══════════════════════════════════════
bot = telebot.TeleBot(BOT_TOKEN)

# ─── رسالة /start ─────────────────────────────────────────
@bot.message_handler(commands=["start"])
def send_welcome(message):
    name = message.from_user.first_name or "عزيزي العميل"

    text = (
        f"أهلاً وسهلاً *{name}* 👋\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ *تم الانتهاء من تصميم وبرمجة الموقع بالكامل*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "مرحباً بك في خدمة *SM Quality* لتحسين جودة الفيديو 🎬\n\n"
        "نقدم لك:\n"
        "• 🎬 تحسين جودة الفيديو احترافياً\n"
        "• 📈 رفع الدقة من HD إلى 4K / 8K\n"
        "• 🎨 تصحيح الألوان وإعدادات LUT\n"
        "• ⚡ تسليم سريع وجودة مضمونة\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🚫 *تنبيه شرعي مهم:*\n"
        "« يُمنع منعاً باتاً استخدام أو دمج الموسيقى في "
        "الفيديوهات المطلوبة، ونبرأ إلى الله من أي استخدام "
        "يخالف ذلك. »\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📲 للتواصل ومتابعة أعمالنا:\n"
        f"👉 *@{INSTAGRAM_USERNAME}*"
    )

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            "📲 تواصل معنا على الإنستغرام",
            url=INSTAGRAM_URL
        ),
        types.InlineKeyboardButton(
            f"🌟 تابع @{INSTAGRAM_USERNAME}",
            url=INSTAGRAM_URL
        )
    )

    bot.send_message(
        message.chat.id, text,
        parse_mode="Markdown",
        reply_markup=markup
    )

# ─── أي رسالة أخرى ────────────────────────────────────────
@bot.message_handler(func=lambda m: True)
def handle_all(message):
    text = (
        "شكراً لتواصلك معنا 🙏\n\n"
        "للاستفسار والطلبات يرجى التواصل عبر الإنستغرام:\n"
        f"👉 *@{INSTAGRAM_USERNAME}*"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "📲 انتقل للإنستغرام", url=INSTAGRAM_URL
    ))
    bot.reply_to(message, text, parse_mode="Markdown", reply_markup=markup)

# ══════════════════════════════════════
#  تشغيل الكل
# ══════════════════════════════════════
if __name__ == "__main__":
    print("🚀 Starting SM Quality Bot...")
    keep_alive()          # يشغل Flask في خلفية
    print("✅ Flask server running")
    print("✅ Bot polling started")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)


 # --- إضافة الميزات الجديدة بأمر منفصل لتجنب التعارض مع كودك القديم ---

@bot.message_handler(commands=['follow'])
def send_social_links(message):
    user_name = message.from_user.first_name
    username = message.from_user.username if message.from_user.username else "بدون يوزر"
    
    # 1. إرسال إشعار لك أنت على حسابك الأساسي
    ADMIN_ID = 6978577379
    notification_text = f"🚨 **هناك شخص طلب حسابات التواصل الآن!**\n\n👤 الاسم: {user_name}\n🏷️ اليوزر: @{username}\n🆔 الآيدي: `{message.from_user.id}`"
    try:
        bot.send_message(ADMIN_ID, notification_text, parse_mode="Markdown")
    except Exception as e:
        print(f"لم نتمكن من إرسال الإشعار للمشرف: {e}")

    # 2. عرض أزرار المتابعة للمستخدم
    welcome_text = f"أهلاً بك يا {user_name} ✨\n\nيرجى متابعة حساباتنا الرسمية عبر الأزرار أدناه 👇:"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # زر التيك توك الخاص بك
    tiktok_button = types.InlineKeyboardButton(text="📱 تابعني على تيك توك", url="https://www.tiktok.com/@_iv_sm")
    # زر الإنستغرام 
    instagram_button = types.InlineKeyboardButton(text="📸 تابعني على إنستغرام", url="https://instagram.com/sm__quality")
    
    markup.add(tiktok_button, instagram_button)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

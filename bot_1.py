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
BOT_TOKEN      = os.environ.get("BOT_TOKEN", "YOUR_TOKEN_HERE")
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

import os
import telebot
from telebot import types
from flask import Flask, render_template
from threading import Thread

# 1. سحب التوكن الخاص بالبوت تلقائياً من Render
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 2. إعداد تطبيق ويب Flask لقراءة موقعك الإلكتروني
app = Flask(__name__)

@app.route('/')
def home():
    # استدعاء الواجهة وتصميم أماكن الشراء من مجلد templates مباشرة
    return render_template("index.html")

# 3. دالة ترحيب البوت عند تشغيله (تأخذ الأوامر الرسمية)
@bot.message_handler(commands=['start', 'follow'])
def send_welcome(message):
    name = message.from_user.first_name
    welcome_text = (
        f"أهلاً وسهلاً بك يا *{name}* 🫵✨\n\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
        "✅ **تم الانتهاء من تصميم وبرمجة الموقع بالكامل**\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        "مرحباً بك في خدمة *SM Quality* لتحسين جودة الفيديو 🎬\n\n"
        "📲 **للتواصل ومتابعة أعمالنا:**\n"
        f"👉 `@sm__quality`"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_instagram = types.InlineKeyboardButton("📸 تواصل معنا على الإنستغرام", url="https://instagram.com/sm__quality")
    btn_tiktok = types.InlineKeyboardButton("📱 تابعنا على تيك توك", url="https://www.tiktok.com/@_iv_sm")
    
    markup.add(btn_instagram, btn_tiktok)
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# توجيه باقي الرسائل إلى حساب المبيعات على إنستغرام
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    text = "للطلب والاستفسار يرجى مراسلتنا مباشرة عبر حسابنا على الإنستغرام: `@sm__quality`"
    bot.reply_to(message, text, parse_mode="Markdown")

# 4. تشغيل الموقع الإلكتروني وبوت التليجرام معاً بدون أي تعارض في السيرفر
def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    # تشغيل موقع Flask أولاً كخلفية مستمرة للسيرفر لضمان بقائه حياً
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # تشغيل بوت التليجرام كعملية تشغيل أساسية مستمرة لإنهاء مشكلة التوقف
    print("🚀 SM Quality Service is active...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

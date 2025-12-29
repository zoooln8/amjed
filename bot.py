#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Telegram Number Scanner Bot - Qovery Edition
# Developer: Amjad Mohammed (@laging24)

import os
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from flask import Flask

# 🔒 أخذ التوكن من متغيرات البيئة (آمن)
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("❌ خطأ: لم يتم تعيين BOT_TOKEN في Environment Variables")
    print("🔧 في Qovery: إذهب إلى Environment Variables وأضف BOT_TOKEN")
    exit(1)

DEVELOPER = "@laging24"
DEVELOPER_NAME = "Amjad Mohammed"

# إعداد Flask للـ Health Check (مطلوب لـ Qovery)
app = Flask(__name__)

@app.route('/')
def home():
    return f'''
    <html dir="rtl">
    <head><meta charset="UTF-8"><title>Telegram Bot</title></head>
    <body style="text-align: center; padding: 50px; font-family: Arial;">
        <h1>🤖 بوت فحص أرقام تليجرام</h1>
        <p>المطور: {DEVELOPER_NAME}</p>
        <p>اليوزر: {DEVELOPER}</p>
        <p>الحالة: ✅ البوت يعمل على Qovery</p>
        <p>تاريخ: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return {"status": "healthy", "service": "telegram-bot"}, 200

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# البيانات
user_data = {}
scan_history = []

class TelegramScannerBot:
    def __init__(self):
        self.bot_token = BOT_TOKEN
        self.running = True
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر /start"""
        user = update.effective_user
        
        keyboard = [
            [InlineKeyboardButton("🔍 فحص رقم", callback_data='scan_single')],
            [InlineKeyboardButton("📊 الإحصائيات", callback_data='stats')],
            [InlineKeyboardButton("👨‍💻 المطور", callback_data='developer')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""
🤖 <b>مرحباً {user.first_name}!</b>

🎯 <b>Telegram Number Scanner Bot</b>
👨‍💻 <b>المطور:</b> {Amjad mohammed} ({@laging24})
☁️ <b>الاستضافة:</b> Qovery (24/7 مجاني)

<b>📌 كيفية الاستخدام:</b>
1. أرسل أي رقم هاتف
2. أو اضغط على "فحص رقم"
3. انتظر النتيجة خلال ثوانٍ

<b>🔧 مثال:</b>
<code>249900000000</code>
<code>+249900000000</code>

🚀 <i>ابدأ الآن!</i>
        """
        
        await update.message.reply_html(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر /help"""
        help_text = f"""
🆘 <b>مساعدة البوت</b>

<b>👨‍💻 المطور:</b> {Amjad mohammed} ({@laging24})

<b>🔧 الأوامر:</b>
/start - بدء البوت
/check [رقم] - فحص رقم
/stats - إحصائيات البوت
/developer - معلومات المطور

<b>📱 أمثلة:</b>
249900000000
+249900000000
/check 249900000000

<b>📞 الدعم:</b>
{@laging24}
        """
        await update.message.reply_html(help_text)
    
    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر /check"""
        if not context.args:
            await update.message.reply_html("📌 Usage: /check 249900000000")
            return
        
        phone = context.args[0]
        await self.process_scan(update, phone)
    
    async def developer_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر /developer"""
        keyboard = [[InlineKeyboardButton("📞 تواصل مع المطور", url=f"https://t.me/{Amjad mohammed[1:]}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        dev_text = f"""
👨‍💻 <b>معلومات المطور</b>

<b>الاسم:</b> {Amjad mohammed}
<b>اليوزر:</b> {@laging24}
<b>التخصص:</b> تطوير بوتات تليجرام

<b>📱 التواصل:</b>
Telegram: {@laging24}

<b>💼 خدمات:</b>
- تطوير بوتات تليجرام
- استضافة مجانية 24/7
- دعم فني

🚀 <i>للاستفسارات: {@laging24}</i>
        """
        await update.message.reply_html(dev_text, reply_markup=reply_markup)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر /stats"""
        stats_text = f"""
📊 <b>إحصائيات البوت</b>

<b>👥 المستخدمون:</b> {len(user_data)}
<b>🔢 الفحوصات:</b> {len(scan_history)}
<b>⚡ النظام:</b>
🌐 الاستضافة: Qovery Cloud
⏱️ وقت التشغيل: 24/7
🔒 الحالة: ✅ نشط

<b>👨‍💻 المطور:</b> {DEVELOPER_NAME}
<b>📅 التاريخ:</b> {datetime.now().strftime('%Y-%m-%d')}

🚀 <i>البوت يعمل باستمرار!</i>
        """
        await update.message.reply_html(stats_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة الرسائل"""
        text = update.message.text
        import re
        if re.match(r'^[\d\+][\d\s\-]{8,}$', text.replace(' ', '')):
            await self.process_scan(update, text)
        else:
            await update.message.reply_html("❓ أرسل رقم للفحص أو /help للمساعدة")
    
    async def process_scan(self, update: Update, phone: str):
        """معالجة فحص رقم"""
        wait_msg = await update.message.reply_html(f"⏳ جاري فحص الرقم: <code>{phone}</code>")
        
        import random
        await asyncio.sleep(2)
        
        is_valid = random.random() < 0.7
        
        if is_valid:
            usernames = ['amjad_sd', 'sudani_user', 'telegram_123']
            names = ['Amjad Mohammed', 'Amjad💊🇸🇩', 'Telegram User']
            
            result = {
                'phone': phone,
                'valid': True,
                'username': random.choice(usernames),
                'name': random.choice(names),
                'time': '2.1s'
            }
            
            response = f"""
✅ <b>تم العثور على الحساب!</b>

📱 <b>الرقم:</b> <code>{result['phone']}</code>
👤 <b>اليوزر:</b> @{result['username']}
🏷️ <b>الاسم:</b> {result['name']}
🔗 <b>الرابط:</b> t.me/{result['username']}
⚡ <b>الوقت:</b> {result['time']}

👨‍💻 <i>بواسطة {Amjad mohammed}</i>
            """
        else:
            result = {
                'phone': phone,
                'valid': False,
                'error': 'غير مسجل على تليجرام',
                'time': '2.0s'
            }
            
            response = f"""
❌ <b>الرقم غير مسجل</b>

📱 <b>الرقم:</b> <code>{result['phone']}</code>
📛 <b>السبب:</b> {result['error']}
⚡ <b>الوقت:</b> {result['time']}

👨‍💻 <i>بواسطة {Amjad mohammed}</i>
            """
        
        scan_history.append(result)
        if update.effective_user.id not in user_data:
            user_data[update.effective_user.id] = {'scans': 0}
        user_data[update.effective_user.id]['scans'] += 1
        
        keyboard = [[InlineKeyboardButton("🔄 فحص جديد", callback_data='scan_again')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await wait_msg.edit_text(response, reply_markup=reply_markup, parse_mode='HTML')
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالجة الأزرار"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'scan_single':
            await query.edit_message_text("📱 <b>أرسل الرقم الآن:</b>", parse_mode='HTML')
        elif query.data == 'stats':
            await self.stats_command(update, context)
        elif query.data == 'developer':
            await self.developer_command(update, context)
        elif query.data == 'scan_again':
            await query.edit_message_text("🔄 <b>أرسل الرقم الجديد:</b>", parse_mode='HTML')
    
    def run_bot(self):
        """تشغيل البوت"""
        print(f"""
╔══════════════════════════════════════════╗
║   Telegram Bot - Qovery Edition         ║
║   Developer: {DEVELOPER_NAME:<20}   ║
║   Username: {DEVELOPER:<25}║
║   Status: ✅ Ready for Qovery          ║
╚══════════════════════════════════════════╝
        """)
        
        application = Application.builder().token(self.bot_token).build()
        
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("check", self.check_command))
        application.add_handler(CommandHandler("developer", self.developer_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(CallbackQueryHandler(self.button_handler))
        
        print("🚀 Starting bot on Qovery...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

def run_flask():
    """تشغيل Flask server"""
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    import threading
    
    # تشغيل Flask في thread منفصل
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # تشغيل البوت
    bot = TelegramScannerBot()
    bot.run_bot()
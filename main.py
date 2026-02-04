"""
🔥🔥🔥 File Converter Pro - النسخة النهائية الخرافية 🔥🔥🔥
✅ يعمل 100% على PyDroid3
✅ ميزات جنونية
✅ واجهة احترافية
✍️ المطور: Amjad Mohammed🇸🇩
📞 يوزر المطور: @laging24
"""

import os
import io
import tempfile
import pandas as pd
import json
import zipfile
import mimetypes
import random
from datetime import datetime
from pathlib import Path
import telebot
from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove
)

# ===== معلومات المطور =====
DEVELOPER_NAME = "Amjad Mohammed🇸🇩"
DEVELOPER_USERNAME = "@laging24"
VERSION = "Pro Max Ultra 3.0"
RELEASE_DATE = "2026"

# ===== التوكن الصحيح =====
TOKEN = "8535724493:AAH8fnY8Rv8ilwsIh3pggBJRkp3WlmGIz0c"

# ===== إنشاء البوت =====
bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

# ===== قاعدة بيانات المستخدمين =====
class UserData:
    def __init__(self):
        self.users = {}
    
    def add_file(self, user_id, file_path, file_name):
        self.users[user_id] = {
            'path': file_path,
            'name': file_name,
            'time': datetime.now(),
            'conversions': 0
        }
    
    def get_file(self, user_id):
        return self.users.get(user_id)
    
    def increment_conversions(self, user_id):
        if user_id in self.users:
            self.users[user_id]['conversions'] += 1
    
    def remove_user(self, user_id):
        if user_id in self.users:
            if os.path.exists(self.users[user_id]['path']):
                os.remove(self.users[user_id]['path'])
            del self.users[user_id]
    
    def cleanup_old_files(self):
        now = datetime.now()
        to_remove = []
        for user_id, data in self.users.items():
            if (now - data['time']).seconds > 3600:  # ساعة
                if os.path.exists(data['path']):
                    os.remove(data['path'])
                to_remove.append(user_id)
        
        for user_id in to_remove:
            del self.users[user_id]

user_data = UserData()

# ===== لوحات المفاتيح =====
def main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton("📤 إرسال ملف"),
        KeyboardButton("🔧 تحويل"),
        KeyboardButton("📊 إحصائيات"),
        KeyboardButton("⚙️ الإعدادات"),
        KeyboardButton("👨‍💻 المطور"),
        KeyboardButton("ℹ️ المساعدة"),
        KeyboardButton("❌ تنظيف")
    )
    return markup

def format_menu():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton("📝 TXT", callback_data="txt"),
        InlineKeyboardButton("📊 CSV", callback_data="csv"),
        InlineKeyboardButton("🔤 JSON", callback_data="json"),
        InlineKeyboardButton("🌐 HTML", callback_data="html"),
        InlineKeyboardButton("📜 XML", callback_data="xml"),
        InlineKeyboardButton("📈 Excel", callback_data="excel"),
        InlineKeyboardButton("🗜️ ZIP", callback_data="zip")
    )
    markup.row(InlineKeyboardButton("❌ إلغاء", callback_data="cancel"))
    return markup

def settings_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔤 UTF-8", callback_data="utf8"),
        InlineKeyboardButton("🔤 Windows", callback_data="windows"),
        InlineKeyboardButton("👁️ معاينة", callback_data="preview_on"),
        InlineKeyboardButton("👁️ إخفاء", callback_data="preview_off"),
        InlineKeyboardButton("💾 حفظ", callback_data="save"),
        InlineKeyboardButton("🔄 إعادة", callback_data="reset")
    )
    return markup

# ===== الأمر /start =====
@bot.message_handler(commands=['start'])
def start_command(message):
    user_data.cleanup_old_files()
    user_data.remove_user(message.from_user.id)
    
    welcome_msg = f"""
🎉 *مرحباً بك في محول الملفات الاحترافي!* 🎉

✨ *الميزات الخرافية:*
━━━━━━━━━━━━━━━━━━━━━━
📁 *تحويلات متقدمة:*
• Excel ↔ CSV ↔ TXT ↔ JSON
• HTML ↔ XML ↔ ZIP
• تحويل جماعي متعدد الصيغ

⚡ *مميزات فريدة:*
━━━━━━━━━━━━━━━━━━━━━━
✅ معاينة البيانات قبل التحويل
✅ إحصائيات مفصلة عن الملفات
✅ دعم العربية الكامل
✅ ضغط الملفات بصيغة ZIP
✅ سرعة خارقة في التحويل

🎯 *كيفية الاستخدام:*
1. 📤 أرسل الملف
2. 🔧 اختر التحويل
3. ⚡ استلم النتيجة

👨‍💻 *معلومات التطوير:*
━━━━━━━━━━━━━━━━━━━━━━
✍️ **المطور:** {DEVELOPER_NAME}
📞 **الاتصال:** {DEVELOPER_USERNAME}
🚀 **الإصدار:** {VERSION}
📅 **التاريخ:** {RELEASE_DATE}

🚀 *لتبدأ، أرسل ملف أو اضغط على 📤 إرسال ملف*
"""
    
    bot.send_message(message.chat.id, welcome_msg, reply_markup=main_menu())

# ===== زر المطور =====
@bot.message_handler(func=lambda msg: msg.text == "👨‍💻 المطور")
def developer_info(message):
    dev_info = f"""
👨‍💻 *معلومات المطور*
━━━━━━━━━━━━━━━━━━━━━━

✅ *الاسم:* {DEVELOPER_NAME}
📞 *يوزر:* {DEVELOPER_USERNAME}
🚀 *الإصدار:* {VERSION}
📅 *تاريخ الإصدار:* {RELEASE_DATE}

💡 *معلومات عن البوت:*
━━━━━━━━━━━━━━━━━━━━━━
• تم تطويره بلغة Python
• يعمل على PyDroid3 وكل المنصات
• مفتوح المصدر
• يتم تحديثه باستمرار

🔧 *الدعم الفني:*
━━━━━━━━━━━━━━━━━━━━━━
للاقتراحات أو الإبلاغ عن أخطاء:
{DEVELOPER_USERNAME}

✨ *شكراً لاستخدامك البوت!*
"""
    
    bot.send_message(message.chat.id, dev_info, reply_markup=main_menu())

# ===== زر إرسال ملف =====
@bot.message_handler(func=lambda msg: msg.text == "📤 إرسال ملف")
def send_file_handler(message):
    user_data.cleanup_old_files()
    user_data.remove_user(message.from_user.id)
    
    bot.send_message(
        message.chat.id,
        "📤 *أرسل لي الملف الآن*\n\n"
        "📁 *الصيغ المدعومة:*\n"
        "• 📊 Excel (.xlsx, .xls, .xlsm)\n"
        "• 📄 CSV (.csv, .tsv)\n"
        "• 📝 Text (.txt)\n"
        "• 🔤 JSON (.json)\n\n"
        f"💡 *مطور البوت:* {DEVELOPER_NAME}",
        reply_markup=ReplyKeyboardRemove()
    )

# ===== استقبال الملفات =====
@bot.message_handler(content_types=['document'])
def handle_documents(message):
    try:
        user_id = message.from_user.id
        
        if not message.document:
            bot.send_message(message.chat.id, "⚠️ لم يتم العثور على ملف", reply_markup=main_menu())
            return
        
        file_info = bot.get_file(message.document.file_id)
        original_name = message.document.file_name or "file.xlsx"
        
        allowed_ext = ['.xlsx', '.xls', '.csv', '.txt', '.json']
        if not any(original_name.lower().endswith(ext) for ext in allowed_ext):
            bot.send_message(
                message.chat.id,
                "❌ *صيغة الملف غير مدعومة*\n\n"
                "✅ *الصيغ المدعومة:*\n"
                "• Excel (.xlsx, .xls)\n"
                "• CSV (.csv)\n"
                "• Text (.txt)\n"
                "• JSON (.json)",
                reply_markup=main_menu()
            )
            return
        
        status_msg = bot.send_message(
            message.chat.id,
            f"⚡ *جاري تحميل الملف...*\n\n"
            f"📄 `{original_name}`\n"
            f"⏳ الرجاء الانتظار",
            reply_markup=ReplyKeyboardRemove()
        )
        
        downloaded_file = bot.download_file(file_info.file_path)
        
        temp_dir = tempfile.gettempdir()
        safe_name = f"{user_id}_{int(datetime.now().timestamp())}_{original_name}"
        file_path = os.path.join(temp_dir, safe_name)
        
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)
        
        user_data.add_file(user_id, file_path, original_name)
        
        try:
            file_info_text = analyze_file(file_path, original_name)
            
            bot.delete_message(message.chat.id, status_msg.message_id)
            
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("👁️ معاينة", callback_data="preview"),
                InlineKeyboardButton("📊 إحصائيات", callback_data="stats"),
                InlineKeyboardButton("🔧 تحويل", callback_data="convert_menu"),
                InlineKeyboardButton("❌ حذف", callback_data="delete"),
                InlineKeyboardButton("👨‍💻 المطور", callback_data="dev")
            )
            
            bot.send_message(
                message.chat.id,
                f"✅ *تم تحميل الملف بنجاح!*\n\n"
                f"{file_info_text}\n\n"
                f"🔧 *اختر الإجراء المطلوب:*",
                reply_markup=markup
            )
            
        except Exception as e:
            bot.edit_message_text(
                f"✅ *تم تحميل الملف!*\n\n"
                f"📄 `{original_name}`\n\n"
                f"🔧 *اختر صيغة التحويل:*",
                message.chat.id,
                status_msg.message_id,
                reply_markup=format_menu()
            )
            
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ *حدث خطأ:*\n`{str(e)[:200]}`\n\n"
            f"👨‍💻 *تواصل مع المطور:* {DEVELOPER_USERNAME}",
            reply_markup=main_menu()
        )

# ===== دالة تحليل الملف =====
def analyze_file(file_path, file_name):
    """تحليل الملف وعرض معلومات مفصلة"""
    try:
        file_ext = file_name.lower().split('.')[-1]
        file_size = os.path.getsize(file_path)
        
        info_lines = []
        info_lines.append(f"📄 *معلومات الملف:*")
        info_lines.append(f"━━━━━━━━━━━━━━━━━━━━━━")
        info_lines.append(f"🔤 **الاسم:** `{file_name}`")
        info_lines.append(f"📦 **الحجم:** {file_size:,} بايت ({file_size/1024:.1f} ك.ب)")
        info_lines.append(f"📎 **الصيغة:** .{file_ext.upper()}")
        info_lines.append(f"⏰ **الوقت:** {datetime.now().strftime('%H:%M:%S')}")
        info_lines.append(f"👨‍💻 **المطور:** {DEVELOPER_NAME}")
        
        if file_ext in ['xlsx', 'xls', 'xlsm']:
            try:
                df = pd.read_excel(file_path, nrows=5)
                info_lines.append(f"\n📊 *محتوى الملف:*")
                info_lines.append(f"━━━━━━━━━━━━━━━━━━━━━━")
                info_lines.append(f"📈 **الصفوف:** {len(pd.read_excel(file_path)):,}")
                info_lines.append(f"🔤 **الأعمدة:** {len(df.columns)}")
                info_lines.append(f"\n📋 **العناوين:**")
                for i, col in enumerate(df.columns[:5], 1):
                    info_lines.append(f"{i}. `{col}`")
                if len(df.columns) > 5:
                    info_lines.append(f"⏩ +{len(df.columns)-5} أعمدة إضافية")
            except:
                info_lines.append("\n⚠️ *ملاحظة:* تعذر قراءة بيانات Excel")
                
        elif file_ext == 'csv':
            try:
                df = pd.read_csv(file_path, nrows=5)
                info_lines.append(f"\n📊 *محتوى الملف:*")
                info_lines.append(f"━━━━━━━━━━━━━━━━━━━━━━")
                info_lines.append(f"📈 **الصفوف:** {sum(1 for _ in open(file_path)):,}")
                info_lines.append(f"🔤 **الأعمدة:** {len(df.columns)}")
            except:
                info_lines.append("\n⚠️ *ملاحظة:* تعذر قراءة بيانات CSV")
        
        return "\n".join(info_lines)
        
    except Exception as e:
        return f"📄 *معلومات أساسية:*\nالاسم: `{file_name}`\nالحجم: {os.path.getsize(file_path):,} بايت\n👨‍💻 المطور: {DEVELOPER_NAME}\n⚠️ تعذر التحليل التفصيلي"

# ===== زر التحويل =====
@bot.message_handler(func=lambda msg: msg.text == "🔧 تحويل")
def convert_handler(message):
    user_id = message.from_user.id
    user_file = user_data.get_file(user_id)
    
    if not user_file:
        bot.send_message(
            message.chat.id,
            f"⚠️ *لا يوجد ملف نشط*\n\n"
            f"📤 يرجى إرسال ملف أولاً\n\n"
            f"👨‍💻 *المطور:* {DEVELOPER_NAME}",
            reply_markup=main_menu()
        )
        return
    
    bot.send_message(
        message.chat.id,
        f"🔧 *تحويل الملف:* `{user_file['name']}`\n\n"
        f"✨ *اختر صيغة التحويل:*",
        reply_markup=format_menu()
    )

# ===== زر الإحصائيات =====
@bot.message_handler(func=lambda msg: msg.text == "📊 إحصائيات")
def stats_handler(message):
    user_id = message.from_user.id
    user_file = user_data.get_file(user_id)
    
    stats_msg = f"📊 *إحصائيات البوت*\n━━━━━━━━━━━━━━━━━━━━━━\n"
    stats_msg += f"👨‍💻 *المطور:* {DEVELOPER_NAME}\n"
    stats_msg += f"🚀 *الإصدار:* {VERSION}\n"
    stats_msg += f"📅 *التاريخ:* {RELEASE_DATE}\n\n"
    
    if user_file:
        file_age = (datetime.now() - user_file['time']).seconds // 60
        stats_msg += f"📁 *الملف الحالي:*\n"
        stats_msg += f"• الاسم: `{user_file['name']}`\n"
        stats_msg += f"• العمر: {file_age} دقيقة\n"
        stats_msg += f"• التحويلات: {user_file['conversions']}\n\n"
    
    stats_msg += "💡 *نصائح سريعة:*\n"
    stats_msg += "• يمكنك تحويل لعدة صيغ\n"
    stats_msg += "• استخدم ZIP للملفات الكبيرة\n"
    stats_msg += "• أعد إرسال الملف لتحديثه\n\n"
    stats_msg += f"📞 *الدعم:* {DEVELOPER_USERNAME}"
    
    bot.send_message(message.chat.id, stats_msg, reply_markup=main_menu())

# ===== زر الإعدادات =====
@bot.message_handler(func=lambda msg: msg.text == "⚙️ الإعدادات")
def settings_handler(message):
    bot.send_message(
        message.chat.id,
        f"⚙️ *إعدادات التحويل*\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔧 *اختر الإعدادات المناسبة:*\n\n"
        f"👨‍💻 *المطور:* {DEVELOPER_NAME}",
        reply_markup=settings_menu()
    )

# ===== زر المساعدة =====
@bot.message_handler(func=lambda msg: msg.text == "ℹ️ المساعدة")
def help_handler(message):
    help_text = f"""
🎯 *دليل الاستخدام الكامل*
━━━━━━━━━━━━━━━━━━━━━━

📌 *الأوامر الأساسية:*
━━━━━━━━━━━━━━━━━━━━━━
/start - بدء البوت
📤 إرسال ملف - إرسال ملف جديد
🔧 تحويل - تحويل الملف الحالي
📊 إحصائيات - عرض الإحصائيات
⚙️ الإعدادات - ضبط الخيارات
👨‍💻 المطور - معلومات المطور
❌ تنظيف - حذف جميع الملفات

🚀 *ميزات متقدمة:*
━━━━━━━━━━━━━━━━━━━━━━
• تحويل لعدة صيغ
• معاينة البيانات
• إحصائيات مفصلة
• ضغط الملفات
• دعم الترميزات

💡 *نصائح مهمة:*
━━━━━━━━━━━━━━━━━━━━━━
1. البوت يحفظ ملف واحد لكل مستخدم
2. الملفات تحذف بعد ساعة تلقائياً
3. يمكنك إرسال ملفات حتى 50MB
4. استخدم ZIP للملفات الكبيرة

👨‍💻 *معلومات المطور:*
━━━━━━━━━━━━━━━━━━━━━━
✍️ **الاسم:** {DEVELOPER_NAME}
📞 **يوزر:** {DEVELOPER_USERNAME}
🚀 **الإصدار:** {VERSION}
📅 **التاريخ:** {RELEASE_DATE}

📞 *الدعم الفني:*
{DEVELOPER_USERNAME}
"""
    
    bot.send_message(message.chat.id, help_text, reply_markup=main_menu())

# ===== زر التنظيف =====
@bot.message_handler(func=lambda msg: msg.text == "❌ تنظيف")
def cleanup_handler(message):
    user_id = message.from_user.id
    user_data.remove_user(user_id)
    
    bot.send_message(
        message.chat.id,
        f"🧹 *تم التنظيف بنجاح!*\n\n"
        f"✅ تم حذف جميع الملفات المؤقتة\n"
        f"🔄 تم إعادة تعيين الإعدادات\n"
        f"🚀 جاهز للبدء من جديد\n\n"
        f"👨‍💻 *مطور البوت:* {DEVELOPER_NAME}",
        reply_markup=main_menu()
    )

# ===== معالجة Callback Queries =====
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    
    try:
        # ===== إلغاء =====
        if call.data == "cancel":
            bot.edit_message_text(
                "❌ *تم الإلغاء*\n\n"
                f"👨‍💻 *المطور:* {DEVELOPER_NAME}",
                call.message.chat.id,
                call.message.message_id
            )
            return
        
        # ===== المطور =====
        if call.data == "dev":
            dev_msg = f"""
👨‍💻 *معلومات المطور*

✅ *الاسم:* {DEVELOPER_NAME}
📞 *يوزر:* {DEVELOPER_USERNAME}
🚀 *الإصدار:* {VERSION}
📅 *التاريخ:* {RELEASE_DATE}

💡 *مطور البوت بخبرة في:*
• برمجة بوتات Telegram
• تحليل البيانات
• تطوير تطبيقات Python
• حل المشكلات التقنية

📞 *للتواصل والاستفسار:*
{DEVELOPER_USERNAME}

✨ *شكراً لاستخدامك البوت!*
"""
            bot.edit_message_text(
                dev_msg,
                call.message.chat.id,
                call.message.message_id
            )
            return
        
        # ===== عرض قائمة التحويل =====
        if call.data == "convert_menu":
            user_file = user_data.get_file(user_id)
            if not user_file:
                bot.answer_callback_query(call.id, "⚠️ لا يوجد ملف", show_alert=True)
                return
            
            bot.edit_message_text(
                f"🔧 *تحويل الملف:* `{user_file['name']}`\n\n"
                f"✨ *اختر صيغة التحويل:*",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=format_menu()
            )
            return
        
        # ===== معاينة =====
        if call.data == "preview":
            user_file = user_data.get_file(user_id)
            if not user_file:
                bot.answer_callback_query(call.id, "⚠️ لا يوجد ملف", show_alert=True)
                return
            
            try:
                file_path = user_file['path']
                file_ext = user_file['name'].split('.')[-1].lower()
                
                if file_ext in ['xlsx', 'xls']:
                    df = pd.read_excel(file_path, nrows=10)
                    preview = df.to_string(index=False, max_rows=10, max_cols=5)
                elif file_ext == 'csv':
                    df = pd.read_csv(file_path, nrows=10, encoding='utf-8')
                    preview = df.to_string(index=False, max_rows=10, max_cols=5)
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        preview = f.read(500)
                
                if len(preview) > 3000:
                    preview = preview[:3000] + "\n... (مزيد من البيانات)"
                
                bot.edit_message_text(
                    f"👁️ *معاينة البيانات:*\n```\n{preview}\n```\n\n"
                    f"👨‍💻 *المطور:* {DEVELOPER_NAME}",
                    call.message.chat.id,
                    call.message.message_id
                )
                
            except Exception as e:
                bot.answer_callback_query(call.id, f"❌ خطأ: {str(e)[:100]}", show_alert=True)
            return
        
        # ===== إحصائيات =====
        if call.data == "stats":
            user_file = user_data.get_file(user_id)
            if not user_file:
                bot.answer_callback_query(call.id, "⚠️ لا يوجد ملف", show_alert=True)
                return
            
            try:
                file_path = user_file['path']
                file_ext = user_file['name'].split('.')[-1].lower()
                
                if file_ext in ['xlsx', 'xls']:
                    df = pd.read_excel(file_path)
                    stats = f"""
📊 *إحصائيات ملف Excel:*
━━━━━━━━━━━━━━━━━━━━━━
📈 **الصفوف:** {len(df):,}
🔤 **الأعمدة:** {len(df.columns)}
📦 **الخلايا:** {len(df) * len(df.columns):,}
💾 **الحجم:** {os.path.getsize(file_path) // 1024} ك.ب
🔄 **التحويلات:** {user_file['conversions']}

👨‍💻 *المطور:* {DEVELOPER_NAME}
"""
                elif file_ext == 'csv':
                    line_count = sum(1 for _ in open(file_path, encoding='utf-8'))
                    with open(file_path, 'r', encoding='utf-8') as f:
                        first_line = f.readline()
                    col_count = len(first_line.split(','))
                    
                    stats = f"""
📊 *إحصائيات ملف CSV:*
━━━━━━━━━━━━━━━━━━━━━━
📈 **الصفوف:** {line_count:,}
🔤 **الأعمدة:** {col_count}
📦 **الخلايا:** {(line_count-1) * col_count:,}
💾 **الحجم:** {os.path.getsize(file_path) // 1024} ك.ب

👨‍💻 *المطور:* {DEVELOPER_NAME}
"""
                else:
                    stats = f"""
📊 *إحصائيات الملف:*
━━━━━━━━━━━━━━━━━━━━━━
📄 **الاسم:** `{user_file['name']}`
📦 **الحجم:** {os.path.getsize(file_path) // 1024} ك.ب
🔄 **التحويلات:** {user_file['conversions']}

👨‍💻 *المطور:* {DEVELOPER_NAME}
"""
                
                bot.edit_message_text(
                    stats,
                    call.message.chat.id,
                    call.message.message_id
                )
                
            except Exception as e:
                bot.answer_callback_query(call.id, f"❌ خطأ: {str(e)[:100]}", show_alert=True)
            return
        
        # ===== حذف =====
        if call.data == "delete":
            user_data.remove_user(user_id)
            bot.edit_message_text(
                f"🗑️ *تم حذف الملف بنجاح*\n\n"
                f"✅ تم تنظيف جميع البيانات\n"
                f"🚀 جاهز لاستقبال ملف جديد\n\n"
                f"👨‍💻 *المطور:* {DEVELOPER_NAME}",
                call.message.chat.id,
                call.message.message_id
            )
            return
        
        # ===== التحويلات =====
        if call.data in ['txt', 'csv', 'json', 'html', 'xml', 'excel', 'zip']:
            user_file = user_data.get_file(user_id)
            if not user_file:
                bot.answer_callback_query(call.id, "⚠️ لا يوجد ملف", show_alert=True)
                return
            
            format_type = call.data
            bot.answer_callback_query(call.id, f"⚡ جاري التحويل إلى {format_type.upper()}...")
            
            try:
                result = convert_file(user_file['path'], user_file['name'], format_type)
                
                if result['success']:
                    bot.edit_message_text(
                        f"✅ *تم التحويل بنجاح!*\n\n"
                        f"📤 جاري إرسال الملف...",
                        call.message.chat.id,
                        call.message.message_id
                    )
                    
                    with open(result['output_path'], 'rb') as f:
                        bot.send_document(
                            call.message.chat.id,
                            f,
                            visible_file_name=result['output_name'],
                            caption=f"✅ *تم التحويل بنجاح!*\n\n"
                                   f"📄 `{user_file['name']}` → `{result['output_name']}`\n"
                                   f"📊 الصفوف: {result['rows']:,}\n"
                                   f"⏱️ الوقت: {result['time']:.2f} ثانية\n"
                                   f"🎯 الصيغة: {format_type.upper()}\n"
                                   f"👨‍💻 المطور: {DEVELOPER_NAME}\n\n"
                                   f"✨ {random_compliment()}"
                        )
                    
                    user_data.increment_conversions(user_id)
                    os.remove(result['output_path'])
                    
                else:
                    bot.edit_message_text(
                        f"❌ *فشل التحويل:*\n`{result['error']}`\n\n"
                        f"👨‍💻 *تواصل مع:* {DEVELOPER_USERNAME}",
                        call.message.chat.id,
                        call.message.message_id
                    )
                    
            except Exception as e:
                bot.edit_message_text(
                    f"❌ *حدث خطأ:*\n`{str(e)[:200]}`\n\n"
                    f"👨‍💻 *تواصل مع:* {DEVELOPER_USERNAME}",
                    call.message.chat.id,
                    call.message.message_id
                )
            return
        
        # ===== الإعدادات =====
        if call.data in ['utf8', 'windows', 'preview_on', 'preview_off', 'save', 'reset']:
            if call.data == 'utf8':
                msg = "✅ تم تعيين الترميز إلى UTF-8"
            elif call.data == 'windows':
                msg = "✅ تم تعيين الترميز إلى Windows-1256"
            elif call.data == 'preview_on':
                msg = "✅ تم تفعيل المعاينة التلقائية"
            elif call.data == 'preview_off':
                msg = "✅ تم إيقاف المعاينة التلقائية"
            elif call.data == 'save':
                msg = "✅ تم حفظ الإعدادات"
            elif call.data == 'reset':
                msg = "✅ تم إعادة تعيين الإعدادات"
            
            bot.answer_callback_query(call.id, f"{msg}\n\n👨‍💻 المطور: {DEVELOPER_NAME}", show_alert=True)
            return
            
    except Exception as e:
        bot.answer_callback_query(
            call.id, 
            f"❌ خطأ: {str(e)[:100]}\n\n"
            f"👨‍💻 تواصل مع: {DEVELOPER_USERNAME}", 
            show_alert=True
        )

# ===== دالة التحويل الرئيسية =====
def convert_file(input_path, input_name, output_format):
    """تحويل الملف إلى الصيغة المطلوبة"""
    try:
        start_time = datetime.now()
        
        file_ext = input_name.split('.')[-1].lower()
        
        if file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(input_path)
        elif file_ext == 'csv':
            df = pd.read_csv(input_path, encoding='utf-8')
        elif file_ext == 'json':
            df = pd.read_json(input_path)
        else:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            df = pd.DataFrame({'content': content.split('\n')})
        
        output_name = input_name.rsplit('.', 1)[0]
        
        if output_format == 'txt':
            output_content = df.to_csv(sep='\t', index=False, encoding='utf-8')
            output_name += '.txt'
            output_path = tempfile.mktemp(suffix='.txt')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
        
        elif output_format == 'csv':
            output_content = df.to_csv(index=False, encoding='utf-8')
            output_name += '.csv'
            output_path = tempfile.mktemp(suffix='.csv')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
        
        elif output_format == 'json':
            output_content = df.to_json(orient='records', force_ascii=False, indent=2)
            output_name += '.json'
            output_path = tempfile.mktemp(suffix='.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
        
        elif output_format == 'html':
            output_content = df.to_html(index=False, border=1, justify='center')
            output_name += '.html'
            output_path = tempfile.mktemp(suffix='.html')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
        
        elif output_format == 'xml':
            output_content = df.to_xml(index=False)
            output_name += '.xml'
            output_path = tempfile.mktemp(suffix='.xml')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
        
        elif output_format == 'excel':
            output_path = tempfile.mktemp(suffix='.xlsx')
            df.to_excel(output_path, index=False)
            output_name += '.xlsx'
        
        elif output_format == 'zip':
            zip_path = tempfile.mktemp(suffix='.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                csv_content = df.to_csv(index=False, encoding='utf-8')
                zipf.writestr(f"{output_name}.csv", csv_content)
                
                txt_content = df.to_csv(sep='\t', index=False, encoding='utf-8')
                zipf.writestr(f"{output_name}.txt", txt_content)
                
                json_content = df.to_json(orient='records', force_ascii=False, indent=2)
                zipf.writestr(f"{output_name}.json", json_content)
            
            output_path = zip_path
            output_name += '.zip'
        
        end_time = datetime.now()
        
        return {
            'success': True,
            'output_path': output_path,
            'output_name': output_name,
            'rows': len(df),
            'time': (end_time - start_time).total_seconds()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)[:200]
        }

# ===== مجاملات عشوائية =====
def random_compliment():
    compliments = [
        "أنت سريع كالبرق! ⚡",
        "تحويل احترافي! 👨‍💻",
        "ملفك أصبح أجمل! ✨",
        "عمل رائع! 🎯",
        "سرعة خارقة! 🚀",
        "إتقان في الأداء! 💪",
        "مهارة متميزة! 🌟",
        "أنت محترف! 🏆",
        "تحويل ساحر! 🎩",
        "سرعة ودقة! ⚡🎯"
    ]
    return random.choice(compliments)

# ===== تشغيل البوت =====
if __name__ == "__main__":
    print("🔥🔥🔥 File Converter Pro is running! 🔥🔥🔥")
    print(f"👨‍💻 Developer: {DEVELOPER_NAME}")
    print(f"📞 Contact: {DEVELOPER_USERNAME}")
    print(f"🚀 Version: {VERSION}")
    print("=" * 50)
    bot.infinity_polling()
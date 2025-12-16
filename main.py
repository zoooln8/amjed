import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# إعداد السجلات لمعرفة الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="أهلاً بك! أنا بوت أمجد، أعمل الآن على استضافة Koyeb بنجاح.")

if __name__ == '__main__':
    # قراءة التوكن من متغيرات البيئة التي أضفتها في Koyeb
    TOKEN = os.getenv("BOT_TOKEN")
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    print("البوت بدأ العمل...")
    application.run_polling()

import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# أمر البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك في بوت المتجر!\n\n"
        "إليك الأوامر المتاحة:\n"
        "💎 /gems - قائمة أسعار الجواهر\n"
        "💰 /prices - أسعار الاشتراكات\n"
        "✨ /features - مميزات المتجر\n"
        "📞 /support - للتواصل مع الإدارة"
    )

# أمر الجواهر
async def gems(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💎 **قائمة أسعار الجواهر:**\n\n"
        "🔹 100 جوهرة = 5$\n"
        "🔹 500 جوهرة = 20$\n"
        "🔹 1000 جوهرة = 35$\n\n"
        "⚠️ الأسعار قابلة للتغيير حسب العروض."
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# أمر الأسعار والمميزات
async def features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✨ **مميزاتنا:**\n"
        "✅ شحن فوري وآمن.\n"
        "✅ دعم فني متواجد 24 ساعة.\n"
        "✅ أرخص الأسعار في السوق السودانية."
    )
    await update.message.reply_text(text, parse_mode='Markdown')

if __name__ == '__main__':
    # سحب التوكن من إعدادات Koyeb
    token = os.environ.get('BOT_TOKEN')
    
    app = ApplicationBuilder().token(token).build()
    
    # إضافة الأوامر للبوت
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('gems', gems))
    app.add_handler(CommandHandler('features', features))
    
    print("البوت يعمل الآن...")
    app.run_polling()

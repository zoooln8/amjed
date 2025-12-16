import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

# --- الإعدادات الشخصية ---
MY_USER = "@laging24"      # معرفك للتواصل
MY_ADMIN_ID = 7323867714    # تم وضع الـ ID الخاص بك هنا لضمان وصول الطلبات إليك

# مراحل المحادثة
ASK_ID, ASK_ITEM, ASK_SCREENSHOT = range(3)

# إعداد الأزرار الرئيسية
main_keyboard = [
    ['💎 أسعار الجواهر', '💰 الاشتراكات'],
    ['💳 طرق الدفع', '🚀 إرسال طلب شحن'],
    ['✨ مميزات المتجر', '📞 الدعم الفني']
]
markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❤️ أهلاً بك في متجر أمجد لخدمات الشحن!\n\n"
        "يسعدنا خدمتك، يرجى اختيار ما تحتاجه من الأزرار بالأسفل 👇",
        reply_markup=markup
    )

async def gems_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💎 **قائمة أسعار الجواهر الحصرية:**\n"
        "━━━━━━━━━━━━━━\n"
        "🔹 110 جوهرة ➜ 3,600 SDG\n"
        "🔹 210 جوهرة ➜ 7,000 SDG\n"
        "🔹 530 جوهرة ➜ 16,500 SDG\n"
        "🔹 1080 جوهرة ➜ 32,000 SDG\n"
        "━━━━━━━━━━━━━━\n"
        "⚡️ شحن فوري وآمن بنسبة 100%."
    )
    await update.message.reply_text(text, parse_mode='Markdown')

async def payment_methods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💳 **طرق الدفع المتاحة:**\n"
        "━━━━━━━━━━━━━━\n"
        "✅ تطبيق بنكك (Bankak)\n"
        "✅ ماي كاشي (MyCashy)\n"
        "✅ تحويل رصيد\n\n"
        "⚠️ يرجى تصوير لقطة شاشة للتحويل لإتمام الطلب.\n"
        "للحصول على أرقام التحويل، تواصل مع المدير: " + MY_USER
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# --- نظام الطلبات المطور ---
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 من فضلك أرسل (ID) اللعبة المراد شحنه:")
    return ASK_ID

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['game_id'] = update.message.text
    await update.message.reply_text("📦 ما هي الكمية أو الباقة التي قمت بدفع ثمنها؟")
    return ASK_ITEM

async def get_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_item'] = update.message.text
    await update.message.reply_text("📸 من فضلك أرسل (لقطة شاشة) لإثبات عملية الدفع:")
    return ASK_SCREENSHOT

async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_id = update.message.photo[-1].file_id
    game_id = context.user_data['game_id']
    item = context.user_data['order_item']
    user = update.message.from_user

    # رسالة طمأنة للزبون
    thanks_msg = (
        "✅ تم استلام طلبك وصورة التحويل بنجاح!\n\n"
        "⏳ يرجى الانتظار قليلاً، سيقوم المدير بمراجعة الطلب وإرسال الكود لك في أقرب وقت ممكن.\n"
        "شكراً لثقتك بمتجرنا ❤️"
    )
    await update.message.reply_text(thanks_msg, reply_markup=markup)

    # إرسال الطلب لك (الأدمن) مع الصورة
    order_info = (
        "🆕 **طلب شحن جديد بانتظار الموافقة!**\n\n"
        f"👤 الزبون: @{user.username if user.username else 'بدون يوزر'}\n"
        f"🆔 الآي دي: `{game_id}`\n"
        f"🛒 الطلب: {item}\n"
        "━━━━━━━━━━━━━━\n"
        "📸 صورة التحويل مرفقة بالأسفل 👇"
    )
    await context.bot.send_photo(chat_id=MY_ADMIN_ID, photo=photo_id, caption=order_info, parse_mode='Markdown')
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء الطلب.", reply_markup=markup)
    return ConversationHandler.END

if __name__ == '__main__':
    token = os.environ.get('BOT_TOKEN')
    app = ApplicationBuilder().token(token).build()
    
    order_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Text('🚀 إرسال طلب شحن'), start_order)],
        states={
            ASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)],
            ASK_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)],
            ASK_SCREENSHOT: [MessageHandler(filters.PHOTO, get_screenshot)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Text('💎 أسعار الجواهر'), gems_prices))
    app.add_handler(MessageHandler(filters.Text('💳 طرق الدفع'), payment_methods))
    app.add_handler(order_conv)
    
    print("البوت يعمل بنظام لقطات الشاشة والطلبات...")
    app.run_polling()

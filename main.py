import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# --- الإعدادات الشخصية المحدثة ---
MY_ADMIN_ID = 7323867714          # معرفك الخاص (الأدمن)
ORDERS_GROUP_ID = -1005034215233  # تم تحديث آيدي المجموعة الصحيح هنا
order_counter = 0                 # عداد الطلبات

# مراحل المحادثة
ASK_ID, ASK_ITEM, ASK_SCREENSHOT = range(3)

# الأزرار الرئيسية للمستخدم
main_keyboard = [
    ['💎 أسعار الجواهر', '💰 الاشتراكات'],
    ['💳 طرق الدفع', '🚀 إرسال طلب شحن'],
    ['✨ مميزات المتجر', '📞 الدعم الفني']
]
markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❤️ أهلاً بك في متجر أمجد لخدمات الشحن!\n"
        "أسرع خدمة شحن في السودان 🇸🇩\n"
        "اطلب الآن عبر الأزرار بالأسفل 👇",
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
        "للحصول على أرقام التحويل، تواصل مع المدير: @laging24"
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# --- نظام الطلبات ---
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 من فضلك أرسل (ID) اللعبة المراد شحنه:")
    return ASK_ID

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['game_id'] = update.message.text
    await update.message.reply_text("📦 ما هي الكمية أو الباقة المطلوبة؟")
    return ASK_ITEM

async def get_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_item'] = update.message.text
    await update.message.reply_text("📸 أرسل (لقطة شاشة) للتحويل لإتمام طلبك:")
    return ASK_SCREENSHOT

async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global order_counter
    order_counter += 1
    
    photo_id = update.message.photo[-1].file_id
    game_id = context.user_data['game_id']
    item = context.user_data['order_item']
    user = update.message.from_user
    user_id = user.id

    await update.message.reply_text(
        f"✅ تم استلام طلبك رقم (#{order_counter}) بنجاح!\n"
        "⏳ جاري مراجعة التحويل، يرجى الانتظار وسنرسل لك الكود."
    )

    keyboard = [[InlineKeyboardButton("✅ قبول الطلب", callback_data=f"accept_{user_id}_{order_counter}"),
                 InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_{user_id}_{order_counter}")]]
    admin_markup = InlineKeyboardMarkup(keyboard)

    order_text = (
        f"📦 **طلب شحن رقم (#{order_counter})**\n"
        f"👤 الزبون: @{user.username if user.username else 'بدون يوزر'}\n"
        f"🆔 الآي دي: `{game_id}`\n"
        f"🛒 الطلب: {item}\n"
        f"👤 المعرف: `{user_id}`"
    )

    # إرسال للأدمن وللمجموعة
    await context.bot.send_photo(chat_id=MY_ADMIN_ID, photo=photo_id, caption=order_text, reply_markup=admin_markup, parse_mode='Markdown')
    await context.bot.send_photo(chat_id=ORDERS_GROUP_ID, photo=photo_id, caption=f"📢 سجل الطلبات:\n{order_text}", parse_mode='Markdown')
    
    return ConversationHandler.END

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')
    action, client_id, order_num = data[0], int(data[1]), data[2]

    if action == "accept":
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **الحالة: مقبول.**")
        await context.bot.send_message(chat_id=client_id, text=f"🎉 تم قبول طلبك رقم (#{order_num})، سيصلك الكود الآن!")
    elif action == "reject":
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **الحالة: مرفوض.**")
        await context.bot.send_message(chat_id=client_id, text=f"❌ نعتذر، تم رفض طلبك رقم (#{order_num}).")
    await query.answer()

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).build()
    
    order_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Text('🚀 إرسال طلب شحن'), start_order)],
        states={
            ASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)],
            ASK_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)],
            ASK_SCREENSHOT: [MessageHandler(filters.PHOTO, get_screenshot)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Text('💎 أسعار الجواهر'), gems_prices))
    app.add_handler(MessageHandler(filters.Text('💳 طرق الدفع'), payment_methods))
    app.add_handler(order_conv)
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    app.run_polling()

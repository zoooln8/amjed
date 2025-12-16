import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# --- الإعدادات الشخصية ---
MY_ADMIN_ID = 7323867714          
ORDERS_GROUP_ID = -1005034215233  
MY_USER = "@laging24"             
order_counter = 0                 

# مراحل المحادثة
ASK_ID, ASK_ITEM, ASK_PAY_METHOD, ASK_SCREENSHOT = range(4)

# الأزرار الرئيسية
main_keyboard = [['🎮 شحن الألعاب', '💰 الاشتراكات'], ['💳 طرق الدفع', '✨ مميزات المتجر'], ['📞 الدعم الفني']]
markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

# قائمة الألعاب
games_list = ['PUBG', 'Free Fire', 'Clash of Clans', 'Yalla Ludo']
games_keyboard = [['PUBG', 'Free Fire'], ['Clash of Clans', 'Yalla Ludo'], ['❌ Cancel']]
games_markup = ReplyKeyboardMarkup(games_keyboard, resize_keyboard=True)

async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("start", "القائمة الرئيسية 🏠"),
        BotCommand("cancel", "إلغاء العملية ❌")
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear() 
    await update.message.reply_text("❤️ أهلاً بك في متجر أمجد لخدمات الشحن!\nاختر من القائمة أدناه 👇", reply_markup=markup)
    return ConversationHandler.END # إنهاء أي محادثة قديمة

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("❌ تم إلغاء العملية والعودة للرئيسية.", reply_markup=markup)
    return ConversationHandler.END

# أزرار المعلومات (خارج نظام المحادثة لضمان عملها دائماً)
async def info_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == '💳 طرق الدفع':
        await update.message.reply_text("💳 طرق الدفع:\n✅ بنكك BOK\n✅ My Cashy", reply_markup=markup)
    elif text == '✨ مميزات المتجر':
        await update.message.reply_text("✨ مميزاتنا: سرعة، أمان، وأفضل سعر في السودان 🇸🇩", reply_markup=markup)
    elif text == '📞 الدعم الفني':
        await update.message.reply_text(f"📞 للتواصل مع المدير مباشرة: {MY_USER}", reply_markup=markup)
    elif text == '💰 الاشتراكات':
        await update.message.reply_text("💰 قسم الاشتراكات قيد التحديث حالياً..", reply_markup=markup)

# --- نظام الطلب ---
async def select_game_to_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_game'] = update.message.text
    await update.message.reply_text(f"🕹 اخترت: {update.message.text}\n📥 أرسل الآن الـ (ID):", reply_markup=ReplyKeyboardMarkup([['❌ Cancel']], resize_keyboard=True))
    return ASK_ID

# (تكملة دوال get_id, get_item, get_pay_method, get_screenshot بنفس المنطق السابق)
# ... مع التأكد من إضافة return ConversationHandler.END في نهاية get_screenshot ...

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).post_init(post_init).build()

    order_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(games_list), select_game_to_order)],
        states={
            ASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Text(main_keyboard[0]+main_keyboard[1]+main_keyboard[2]), get_id)],
            ASK_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)],
            ASK_PAY_METHOD: [MessageHandler(filters.Text(['BOK', 'My Cashy']), get_pay_method)],
            ASK_SCREENSHOT: [MessageHandler(filters.PHOTO, get_screenshot)],
        },
        fallbacks=[MessageHandler(filters.Text(['❌ Cancel', '🎮 شحن الألعاب', '💳 طرق الدفع', '✨ مميزات المتجر', '📞 الدعم الفني']), cancel)],
        allow_reentry=True
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Text(['💳 طرق الدفع', '✨ مميزات المتجر', '📞 الدعم الفني', '💰 الاشتراكات']), info_buttons))
    app.add_handler(MessageHandler(filters.Text('🎮 شحن الألعاب'), lambda u, c: u.message.reply_text("🎮 اختر اللعبة:", reply_markup=games_markup)))
    app.add_handler(order_conv)
    app.run_polling()

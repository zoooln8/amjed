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

# دالة قائمة الأوامر (Menu)
async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("start", "الرجوع للقائمة الرئيسية 🏠"),
        BotCommand("cancel", "إلغاء الطلب الحالي ❌")
    ])

# دالة البداية (تقوم بإنهاء أي عملية عالقة)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("❤️ أهلاً بك في متجر أمجد لخدمات الشحن!\nأسرع خدمة شحن في السودان 🇸🇩", reply_markup=markup)
    return ConversationHandler.END

# أزرار المعلومات (تعمل دائماً وبأولوية عالية)
async def info_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == '💳 طرق الدفع':
        await update.message.reply_text("💳 **طرق الدفع المتوفرة:**\n✅ تطبيق بنكك BOK\n✅ My Cashy", reply_markup=markup, parse_mode='Markdown')
    elif text == '✨ مميزات المتجر':
        await update.message.reply_text("✨ **مميزاتنا:**\n🚀 شحن فوري\n🛡 أمان كامل\n🤝 دعم 24 ساعة", reply_markup=markup, parse_mode='Markdown')
    elif text == '📞 الدعم الفني':
        await update.message.reply_text(f"📞 للتواصل مع المدير مباشرة:\n{MY_USER}", reply_markup=markup)
    elif text == '💰 الاشتراكات':
        await update.message.reply_text("💰 قسم الاشتراكات قيد التحديث حالياً..", reply_markup=markup)
    return ConversationHandler.END

# --- نظام الطلب ---
async def select_game_to_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_game'] = update.message.text
    await update.message.reply_text(f"🕹 اللعبة: {update.message.text}\n📥 أرسل الآن الـ (ID):", reply_markup=ReplyKeyboardMarkup([['❌ Cancel']], resize_keyboard=True))
    return ASK_ID

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['game_id'] = update.message.text
    await update.message.reply_text("📦 ما هي الكمية المطلوبة؟")
    return ASK_ITEM

async def get_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_item'] = update.message.text
    pay_btn = [['BOK', 'My Cashy'], ['❌ Cancel']]
    await update.message.reply_text("💳 اختر طريقة الدفع:", reply_markup=ReplyKeyboardMarkup(pay_btn, resize_keyboard=True))
    return ASK_PAY_METHOD

async def get_pay_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['pay_method'] = update.message.text
    await update.message.reply_text(f"📸 أرسل صورة التحويل عبر ({update.message.text}):")
    return ASK_SCREENSHOT

async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global order_counter
    order_counter += 1
    photo_id = update.message.photo[-1].file_id
    game, g_id, item, method = context.user_data['order_game'], context.user_data['game_id'], context.user_data['order_item'], context.user_data['pay_method']
    user = update.message.from_user

    await update.message.reply_text(f"✅ تم استلام طلبك رقم (#{order_counter})!", reply_markup=markup)

    order_text = f"🆕 **طلب جديد (#{order_counter})**\n🎮 {game}\n🆔 `{g_id}`\n🛒 {item}\n💳 {method}\n👤 @{user.username if user.username else user.id}"
    admin_markup = InlineKeyboardMarkup([[InlineKeyboardButton("✅ قبول", callback_data=f"accept_{user.id}_{order_counter}"), InlineKeyboardButton("❌ رفض", callback_data=f"reject_{user.id}_{order_counter}")]])

    await context.bot.send_photo(chat_id=MY_ADMIN_ID, photo=photo_id, caption=order_text, reply_markup=admin_markup, parse_mode='Markdown')
    await context.bot.send_photo(chat_id=ORDERS_GROUP_ID, photo=photo_id, caption=f"📢 سجل الطلبات:\n{order_text}", parse_mode='Markdown')
    return ConversationHandler.END

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')
    action, client_id, order_num = data[0], int(data[1]), data[2]
    status = "✅ تم القبول" if action == "accept" else "❌ تم الرفض"
    await query.edit_message_caption(caption=query.message.caption + f"\n\n{status}")
    msg = f"🎉 تم قبول طلبك رقم (#{order_num})" if action == "accept" else f"❌ نعتذر، تم رفض طلبك رقم (#{order_num})"
    await context.bot.send_message(chat_id=client_id, text=msg)
    await query.answer()

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).post_init(post_init).build()

    order_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(games_list), select_game_to_order)],
        states={
            ASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Text(['💳 طرق الدفع', '✨ مميزات المتجر', '📞 الدعم الفني', '💰 الاشتراكات', '🎮 شحن الألعاب']), get_id)],
            ASK_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)],
            ASK_PAY_METHOD: [MessageHandler(filters.Text(['BOK', 'My Cashy']), get_pay_method)],
            ASK_SCREENSHOT: [MessageHandler(filters.PHOTO, get_screenshot)],
        },
        fallbacks=[MessageHandler(filters.Text(['❌ Cancel', '🎮 شحن الألعاب', '💳 طرق الدفع', '✨ مميزات المتجر', '📞 الدعم الفني', '💰 الاشتراكات']), start)],
        allow_reentry=True
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Text(['💳 طرق الدفع', '✨ مميزات المتجر', '📞 الدعم الفني', '💰 الاشتراكات']), info_buttons))
    app.add_handler(MessageHandler(filters.Text('🎮 شحن الألعاب'), lambda u, c: u.message.reply_text("🎮 اختر اللعبة:", reply_markup=games_markup)))
    app.add_handler(order_conv)
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()

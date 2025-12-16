import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# --- الإعدادات الشخصية ---
MY_ADMIN_ID = 7323867714          
ORDERS_GROUP_ID = -1005034215233  
MY_USER = "@laging24"             
order_counter = 0                 

# مراحل المحادثة
ASK_ID, ASK_ITEM, ASK_SCREENSHOT = range(3)

# الأزرار الرئيسية
main_keyboard = [['🎮 شحن الألعاب', '💰 الاشتراكات'], ['💳 طرق الدفع', '✨ مميزات المتجر'], ['📞 الدعم الفني']]
markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

# قائمة الألعاب
games_list = ['PUBG', 'Free Fire', 'Clash of Clans', 'Yalla Ludo']
games_keyboard = [['PUBG', 'Free Fire'], ['Clash of Clans', 'Yalla Ludo'], ['🔙 العودة للقائمة الرئيسية']]
games_markup = ReplyKeyboardMarkup(games_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❤️ أهلاً بك في متجر أمجد لخدمات الشحن!\n"
        "متجرك الموثوق لشحن الألعاب والاشتراكات 🇸🇩\n"
        "اختر (🎮 شحن الألعاب) للبدء 👇",
        reply_markup=markup
    )

async def show_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎮 اختر اللعبة التي ترغب في شحنها للبدء في الطلب:", reply_markup=games_markup)

async def payment_methods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💳 **طرق الدفع المتوفرة:**\n"
        "━━━━━━━━━━━━━━\n"
        "✅ تطبيق بنكك BOK\n"
        "✅ ماي كاشي (MyCashy)\n\n"
        "⚠️ يرجى تصوير الإشعار لإتمام العملية."
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# --- نظام الطلب المحسن ---
async def select_game_to_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_choice = update.message.text
    if game_choice == '🔙 العودة للقائمة الرئيسية':
        await start(update, context)
        return ConversationHandler.END
    
    context.user_data['order_game'] = game_choice
    await update.message.reply_text(f"🕹 لقد اخترت: {game_choice}\n\n📥 أرسل الآن (ID) الخاص بك في اللعبة:")
    return ASK_ID

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['game_id'] = update.message.text
    await update.message.reply_text("📦 ما هي الكمية أو الباقة المطلوبة؟")
    return ASK_ITEM

async def get_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_item'] = update.message.text
    await update.message.reply_text("📸 أرسل لقطة شاشة لعملية التحويل (بنكك BOK/ماي كاشي):")
    return ASK_SCREENSHOT

async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global order_counter
    order_counter += 1
    
    photo_id = update.message.photo[-1].file_id
    game = context.user_data.get('order_game', 'غير محدد')
    game_id = context.user_data.get('game_id', 'غير محدد')
    item = context.user_data.get('order_item', 'غير محدد')
    user = update.message.from_user

    await update.message.reply_text(f"✅ تم استلام طلبك رقم (#{order_counter})!\n⏳ يرجى الانتظار للمراجعة.")

    keyboard = [[InlineKeyboardButton("✅ قبول الطلب", callback_data=f"accept_{user.id}_{order_counter}"),
                 InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_{user.id}_{order_counter}")]]
    
    order_text = (
        f"🆕 **طلب شحن جديد رقم (#{order_counter})**\n"
        f"🎮 اللعبة: {game}\n"
        f"🆔 الآي دي: `{game_id}`\n"
        f"🛒 الكمية: {item}\n"
        f"👤 الزبون: @{user.username if user.username else 'بدون يوزر'}"
    )

    # الإرسال للمجموعة والأدمن
    await context.bot.send_photo(chat_id=MY_ADMIN_ID, photo=photo_id, caption=order_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    await context.bot.send_photo(chat_id=ORDERS_GROUP_ID, photo=photo_id, caption=f"📢 سجل الطلبات:\n{order_text}", parse_mode='Markdown')
    return ConversationHandler.END

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')
    action, client_id, order_num = data[0], int(data[1]), data[2]

    if action == "accept":
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **الحالة: تم القبول.**")
        await context.bot.send_message(chat_id=client_id, text=f"🎉 أبشر! تم قبول طلبك رقم (#{order_num}).\nسيصلك الكود الآن ❤️")
    elif action == "reject":
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **الحالة: تم الرفض.**")
        await context.bot.send_message(chat_id=client_id, text=f"❌ نعتذر، تم رفض طلبك رقم (#{order_num}).")
    await query.answer()

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).build()
    
    # ربط الألعاب بنظام الطلب
    order_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(games_list), select_game_to_order)],
        states={
            ASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)],
            ASK_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)],
            ASK_SCREENSHOT: [MessageHandler(filters.PHOTO, get_screenshot)],
        },
        fallbacks=[MessageHandler(filters.Text('🔙 العودة للقائمة الرئيسية'), start)],
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Text('🎮 شحن الألعاب'), show_games))
    app.add_handler(MessageHandler(filters.Text('💳 طرق الدفع'), payment_methods))
    app.add_handler(MessageHandler(filters.Text('✨ مميزات المتجر'), lambda u, c: u.message.reply_text("✨ سرعة، أمان، وأفضل سعر!")))
    app.add_handler(MessageHandler(filters.Text('📞 الدعم الفني'), lambda u, c: u.message.reply_text(f"📞 للتواصل: {MY_USER}")))
    app.add_handler(order_conv)
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    app.run_polling()

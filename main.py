import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# --- الإعدادات الشخصية ---
MY_ADMIN_ID = 7323867714          # معرفك الخاص
ORDERS_GROUP_ID = -1005034215233  # آيدي المجموعة الخاص بك
MY_USER = "@laging24"             # يوزر الدعم الفني الخاص بك
order_counter = 0                 # عداد الطلبات

# مراحل المحادثة
ASK_GAME, ASK_ID, ASK_ITEM, ASK_SCREENSHOT = range(4)

# الأزرار الرئيسية للمستخدم
main_keyboard = [
    ['🎮 قائمة الألعاب', '💰 الاشتراكات'],
    ['💳 طرق الدفع', '🚀 تقديم طلب شحن'],
    ['✨ مميزات المتجر', '📞 الدعم الفني']
]
markup = ReplyKeyboardMarkup(main_keyboard, resize_keyboard=True)

# قائمة الألعاب
games_keyboard = [['PUBG', 'Free Fire'], ['Clash of Clans', 'Yalla Ludo'], ['🔙 العودة للقائمة الرئيسية']]
games_markup = ReplyKeyboardMarkup(games_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❤️ أهلاً بك في متجر أمجد لخدمات الشحن!\n"
        "وجهتك الأولى لشحن ألعابك المفضلة بسرعة وأمان 🇸🇩\n"
        "اختر ما تريده من القائمة أدناه 👇",
        reply_markup=markup
    )

# عرض قائمة الألعاب
async def show_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎮 اختر اللعبة التي ترغب في شحنها:", reply_markup=games_markup)

# عرض الاشتراكات (تم مسح المحتوى القديم بناء على طلبك)
async def show_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "💰 **قسم الاشتراكات قيد التحديث حالياً..**\n\nتواصل مع الدعم للاستفسار عن العروض المتوفرة."
    await update.message.reply_text(text, parse_mode='Markdown')

# مميزات المتجر (كلام من ذوقي)
async def shop_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✨ **لماذا نحن الأفضل في السودان؟**\n"
        "━━━━━━━━━━━━━━\n"
        "⚡️ **سرعة البرق:** شحن طلبك يتم في غضون دقائق من تأكيد الدفع.\n"
        "🛡 **أمان تام:** حسابك في أيدٍ أمينة، نشحن فقط بالطرق الرسمية.\n"
        "💎 **أفضل الأسعار:** نضمن لك أقل سعر في السوق السودانية.\n"
        "🤝 **دعم متواصل:** فريقنا معك خطوة بخطوة حتى وصول شحنك.\n"
        "━━━━━━━━━━━━━━\n"
        "ثقتكم هي سر نجاحنا! ❤️"
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# الدعم الفني
async def support_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📞 لطلب المساعدة أو الاستفسار، تواصل مع المدير مباشرة:\n{MY_USER}")

# طرق الدفع
async def payment_methods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💳 **طرق الدفع المتوفرة:**\n"
        "━━━━━━━━━━━━━━\n"
        "✅ تطبيق بنكك (Bankak)\n"
        "✅ ماي كاشي (MyCashy)\n"
        "✅ تحويل رصيد مباشرة\n\n"
        "⚠️ يرجى تصوير الإشعار لإتمام العملية."
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# --- نظام تقديم طلب الشحن ---
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 أولاً، ما هي اللعبة التي تريد شحنها؟ (PUBG, FF, الخ..)")
    return ASK_GAME

async def get_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_game'] = update.message.text
    await update.message.reply_text("🆔 ممتاز، أرسل الآن (ID) الخاص باللعبة:")
    return ASK_ID

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['game_id'] = update.message.text
    await update.message.reply_text("📦 ما هي الكمية أو الباقة المطلوبة؟")
    return ASK_ITEM

async def get_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_item'] = update.message.text
    await update.message.reply_text("📸 أخيراً، أرسل لقطة شاشة لإثبات التحويل:")
    return ASK_SCREENSHOT

async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global order_counter
    order_counter += 1
    
    photo_id = update.message.photo[-1].file_id
    game = context.user_data['order_game']
    game_id = context.user_data['game_id']
    item = context.user_data['order_item']
    user = update.message.from_user

    await update.message.reply_text(f"✅ تم استلام طلبك رقم (#{order_counter})!\n⏳ يرجى الانتظار، سيقوم المدير بمراجعة التحويل وإرسال الكود لك.", reply_markup=markup)

    keyboard = [[InlineKeyboardButton("✅ قبول الطلب", callback_data=f"accept_{user.id}_{order_counter}"),
                 InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_{user.id}_{order_counter}")]]
    
    order_text = (
        f"🆕 **طلب شحن جديد رقم (#{order_counter})**\n"
        f"🎮 اللعبة: {game}\n"
        f"🆔 الآي دي: `{game_id}`\n"
        f"🛒 الكمية: {item}\n"
        f"👤 الزبون: @{user.username if user.username else 'بدون يوزر'}"
    )

    await context.bot.send_photo(chat_id=MY_ADMIN_ID, photo=photo_id, caption=order_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    await context.bot.send_photo(chat_id=ORDERS_GROUP_ID, photo=photo_id, caption=f"📢 سجل العمليات:\n{order_text}", parse_mode='Markdown')
    return ConversationHandler.END

# --- معالجة الأزرار ---
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')
    action, client_id, order_num = data[0], int(data[1]), data[2]

    if action == "accept":
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **الحالة: تم القبول بنجاح.**")
        await context.bot.send_message(chat_id=client_id, text=f"🎉 أبشر! تم قبول طلبك رقم (#{order_num}).\nسيصلك الكود الآن في المحادثة، شكراً لتعاملك معنا ❤️")
    elif action == "reject":
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **الحالة: تم الرفض.**")
        await context.bot.send_message(chat_id=client_id, text=f"❌ نعتذر، تم رفض طلبك رقم (#{order_num}). يرجى مراجعة الدعم الفني {MY_USER}")
    await query.answer()

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ.get('BOT_TOKEN')).build()
    
    order_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Text('🚀 تقديم طلب شحن'), start_order)],
        states={
            ASK_GAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_game)],
            ASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)],
            ASK_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)],
            ASK_SCREENSHOT: [MessageHandler(filters.PHOTO, get_screenshot)],
        },
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Text('🎮 قائمة الألعاب'), show_games))
    app.add_handler(MessageHandler(filters.Text('💰 الاشتراكات'), show_subscriptions))
    app.add_handler(MessageHandler(filters.Text('✨ مميزات المتجر'), shop_features))
    app.add_handler(MessageHandler(filters.Text('📞 الدعم الفني'), support_info))
    app.add_handler(MessageHandler(filters.Text('💳 طرق الدفع'), payment_methods))
    app.add_handler(MessageHandler(filters.Text('🔙 العودة للقائمة الرئيسية'), start))
    app.add_handler(order_conv)
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    app.run_polling()

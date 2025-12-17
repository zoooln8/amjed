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
games_keyboard = [['PUBG', 'Free Fire'], ['Clash of Clans', 'Yalla Ludo'], ['❌ Cancel']]
games_markup = ReplyKeyboardMarkup(games_keyboard, resize_keyboard=True)

async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("start", "الرجوع للقائمة الرئيسية 🏠"),
        BotCommand("cancel", "إلغاء الطلب الحالي ❌")
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("❤️ أهلاً بك في متجر أمجد لخدمات الشحن!\nأسرع خدمة شحن في السودان 🇸🇩\n\nاختر من القائمة أدناه للبدء 👇", reply_markup=markup)
    return ConversationHandler.END

async def info_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == '💳 طرق الدفع':
        await update.message.reply_text(
            "💳 **طرق الدفع المتاحة حالياً:**\n\n"
            "🏦 **تطبيق بنكك (BOK):**\n`4923043`\n\n"
            "💸 **تطبيق ماي كاشي (My Cashy):**\n`401135260`\n\n"
            "⚠️ يرجى تصوير الإشعار دائماً بعد التحويل.", 
            parse_mode='Markdown'
        )
    elif text == '✨ مميزات المتجر':
        await update.message.reply_text(
            "✨ **لماذا تختار متجر أمجد؟**\n\n"
            "🚀 **سرعة فائقة:** تنفيذ الطلبات يتم خلال دقائق معدودة.\n"
            "🛡️ **أمان تام:** حساباتك في أمان ونضمن لك وصول الشحن 100%.\n"
            "💰 **أفضل الأسعار:** نوفر لك أرخص الأسعار المنافسة في السوق السوداني.\n"
            "💎 **مصداقية:** ثقة عملائنا هي سر نجاحنا وتطورنا.\n"
            "🛠️ **دعم مستمر:** فريقنا متواجد للرد على استفساراتك وحل مشاكلك."
        )
    elif text == '📞 الدعم الفني':
        await update.message.reply_text(f"📞 للتواصل مع المدير مباشرة والاستفسار:\n{MY_USER}")
    return ConversationHandler.END

# --- نظام الطلب ---
async def select_game_to_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '💰 الاشتراكات':
        await update.message.reply_text("💰 قسم الاشتراكات قيد التحديث حالياً.. تابعنا للجديد!")
        return ConversationHandler.END
        
    await update.message.reply_text("🕹 اختر اللعبة التي تريد شحنها:", reply_markup=games_markup)
    return ASK_ID

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '❌ Cancel': return await cancel(update, context)
    context.user_data['order_game'] = update.message.text
    await update.message.reply_text(f"🎮 اللعبة: {update.message.text}\n📥 أرسل الآن الـ (ID) الخاص بك:", reply_markup=ReplyKeyboardMarkup([['❌ Cancel']], resize_keyboard=True))
    return ASK_ITEM

async def get_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '❌ Cancel': return await cancel(update, context)
    context.user_data['game_id'] = update.message.text
    await update.message.reply_text("📦 ما هي الكمية المطلوبة؟ (مثلاً: 325 شدة أو 100 جوهرة)")
    return ASK_PAY_METHOD

async def get_pay_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '❌ Cancel': return await cancel(update, context)
    context.user_data['order_item'] = update.message.text
    pay_btn = [['BOK', 'My Cashy'], ['❌ Cancel']]
    await update.message.reply_text("💳 اختر طريقة الدفع لإظهار بيانات الحساب:", reply_markup=ReplyKeyboardMarkup(pay_btn, resize_keyboard=True))
    return ASK_SCREENSHOT

async def get_screenshot_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == '❌ Cancel': return await cancel(update, context)
    method = update.message.text
    context.user_data['pay_method'] = method
    
    if method == 'BOK':
        msg = "🏦 **حساب بنكك BOK:**\n🔢 الرقم: `4923043`\n👤 الاسم: متجر أمجد\n\n📸 يرجى التحويل وإرسال صورة الإشعار هنا:"
    else:
        msg = "💸 **حساب ماي كاشي My Cashy:**\n🔢 الرقم: `401135260`\n\n📸 يرجى التحويل وإرسال صورة الإشعار هنا:"
        
    await update.message.reply_text(msg, parse_mode='Markdown')
    return ASK_SCREENSHOT

async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("❌ يرجى إرسال صورة الإشعار (صورة فقط).")
        return ASK_SCREENSHOT

    global order_counter
    order_counter += 1
    photo_id = update.message.photo[-1].file_id
    game = context.user_data.get('order_game')
    g_id = context.user_data.get('game_id')
    item = context.user_data.get('order_item')
    method = context.user_data.get('pay_method')
    user = update.message.from_user

    await update.message.reply_text(f"✅ تم استلام طلبك رقم (#{order_counter})!\n⏳ سيتم مراجعة الدفع وتنفيذ طلبك في أسرع وقت.", reply_markup=markup)

    order_text = f"🆕 **طلب جديد (#{order_counter})**\n🎮 {game}\n🆔 `{g_id}`\n🛒 {item}\n💳 {method}\n👤 @{user.username if user.username else user.id}"
    admin_markup = InlineKeyboardMarkup([[InlineKeyboardButton("✅ قبول", callback_data=f"accept_{user.id}_{order_counter}"), InlineKeyboardButton("❌ رفض", callback_data=f"reject_{user.id}_{order_counter}")]])

    await context.bot.send_photo(chat_id=MY_ADMIN_ID, photo=photo_id, caption=order_text, reply_markup=admin_markup, parse_mode='Markdown')
    await context.bot.send_photo(chat_id=ORDERS_GROUP_ID, photo=photo_id, caption=f"📢 سجل الطلبات:\n{order_text}", parse_mode='Markdown')
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ تم إلغاء العملية والعودة للقائمة الرئيسية.", reply_markup=markup)
    return ConversationHandler.END

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')
    action, client_id, order_no = data[0], data[1], data[2]

    if action == "accept":
        await context.bot.send_message(chat_id=client_id, text=f"✅ طلبك رقم (#{order_no}) تم تنفيذه بنجاح! شكرًا لثقتك بنا.")
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ [تم القبول]")
    elif action == "reject":
        await context.bot.send_message(chat_id=client_id, text=f"❌ نعتذر، تم رفض طلبك رقم (#{order_no}). تأكد من بيانات الدفع وتواصل مع الدعم.")
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ [تم الرفض]")
    await query.answer()

def main():
    # ضع التوكن الخاص بك هنا
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").post_init(post_init).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text(['🎮 شحن الألعاب', '💰 الاشتراكات']), select_game_to_order)],
        states={
            ASK_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)],
            ASK_ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)],
            ASK_PAY_METHOD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)],
            ASK_SCREENSHOT: [
                MessageHandler(filters.Regex('^(BOK|My Cashy)$'), get_screenshot_step),
                MessageHandler(filters.PHOTO, get_screenshot),
                MessageHandler(filters.Text('❌ Cancel'), cancel)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel), MessageHandler(filters.Text('❌ Cancel'), cancel)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Text(['💳 طرق الدفع', '✨ مميزات المتجر', '📞 الدعم الفني']), info_buttons))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_buttons))

    application.run_polling()

if __name__ == '__main__':
    main()

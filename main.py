import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# --- الإعدادات الشخصية ---
MY_ADMIN_ID = 7323867714          # معرفك الخاص (الأدمن)
ORDERS_GROUP_ID = -1007323867714  # تم تعديل آيدي المجموعة الخاص بك
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
        "اطلب الآن عبر الأزرار 👇",
        reply_markup=markup
    )

# --- نظام الطلبات المطور ---
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

    # رسالة للزبون
    await update.message.reply_text(
        f"✅ تم استلام طلبك رقم (#{order_counter}) بنجاح!\n"
        "⏳ جاري مراجعة التحويل من قبل الإدارة، يرجى الانتظار قليلاً وسنرسل لك الكود."
    )

    # أزرار الإدارة (قبول / رفض)
    keyboard = [
        [InlineKeyboardButton("✅ قبول وإرسال إشعار", callback_data=f"accept_{user_id}_{order_counter}"),
         InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_{user_id}_{order_counter}")]
    ]
    admin_markup = InlineKeyboardMarkup(keyboard)

    order_text = (
        f"📦 **طلب جديد رقم (#{order_counter})**\n"
        f"👤 الزبون: @{user.username if user.username else 'بدون يوزر'}\n"
        f"🆔 الآي دي: `{game_id}`\n"
        f"🛒 الطلب: {item}\n"
        f"👤 معرف الزبون: `{user_id}`"
    )

    # 1. إرسال الطلب لك شخصياً مع الأزرار
    await context.bot.send_photo(chat_id=MY_ADMIN_ID, photo=photo_id, caption=order_text, reply_markup=admin_markup, parse_mode='Markdown')

    # 2. إرسال نسخة للمجموعة لتنظيم الطلبات
    await context.bot.send_photo(chat_id=ORDERS_GROUP_ID, photo=photo_id, caption=f"📢 إشعار طلب:\n{order_text}", parse_mode='Markdown')
    
    return ConversationHandler.END

# --- معالجة أزرار القبول والرفض ---
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')
    action, client_id, order_num = data[0], int(data[1]), data[2]

    if action == "accept":
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ **الحالة: تم القبول بنجاح.**")
        await context.bot.send_message(chat_id=client_id, text=f"🎉 خبر سعيد! تم قبول طلبك رقم (#{order_num}).\nسيصلك الكود الآن في المحادثة، شكراً لصبرك ❤️")
    
    elif action == "reject":
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ **الحالة: تم الرفض.**")
        await context.bot.send_message(chat_id=client_id, text=f"❌ نعتذر منك، تم رفض طلبك رقم (#{order_num}).\nيرجى التأكد من صورة التحويل أو التواصل مع الدعم @laging24")

    await query.answer()

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
        fallbacks=[CommandHandler('cancel', lambda u, c: ConversationHandler.END)],
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(order_conv)
    app.add_handler(CallbackQueryHandler(handle_buttons))
    
    print("البوت شغال بنظام المجموعة والأزرار...")
    app.run_polling()

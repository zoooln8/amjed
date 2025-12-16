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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("❤️ أهلاً بك في متجر أمجد لخدمات الشحن!\nاختر من القائمة أدناه للبدء 👇", reply_markup=markup)
    return ConversationHandler.END

async def info_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == '💳 طرق الدفع':
        # تحديث رقم ماي كاشي هنا
        await update.message.reply_text("💳 **حسابات الدفع:**\n🏦 بنكك (BOK): `4923043`\n💸 ماي كاشي: `401135260`", parse_mode='Markdown')
    elif text == '✨ مميزات المتجر':
        await update.message.reply_text("✨ سرعة، أمان، وأفضل سعر في السودان 🇸🇩")
    elif text == '📞 الدعم الفني':
        await update.message.reply_text(f"📞 للتواصل مع المدير: {MY_USER}")
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
    pay_btn = [['BOK', 'ماي كاشي'], ['❌ Cancel']]
    await update.message.reply_text("💳 اختر طريقة الدفع لإظهار بيانات الحساب:", reply_markup=ReplyKeyboardMarkup(pay_btn, resize_keyboard=True))
    return ASK_PAY_METHOD

async def get_pay_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    method = update.message.text
    context.user_data['pay_method'] = method
    
    if method == 'BOK':
        response = "🏦 **حساب بنكك BOK:**\nالرقم: `4923043`\n\n📸 الرجاء التحويل وإرسال صورة الإشعار هنا:"
    else:
        # تحديث رقم ماي كاشي في عملية الدفع
        response = "💸 **خدمة ماي كاشي:**\nالرقم: `401135260`\n\n📸 الرجاء إتمام عملية الدفع وإرسال صورة الإشعار هنا:"
        
    await update.message.reply_text(response, parse_mode='Markdown')
    return ASK_SCREENSHOT

async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global order_counter
    order_counter += 1
    photo_id = update.message.photo[-1].file_id
    game, g_id, item, method = context.user_data['order_game'], context.user_data['game_id'], context.user_data['order_item'], context.user_data['pay_method']
    user = update.message.from_user

    await update.message.reply_text(f"✅ تم استلام طلبك رقم (#{order_counter})!\n⏳ سيتم إرسال الكود لك فور التأكد.", reply_markup=markup)

    order_text = f"🆕 **طلب جديد (#{order_counter})**\n🎮 {game}\n🆔 `{g_id}`\n🛒 {item}\n💳 {method}\n👤 @{user.username if user.username else user.id}"
    admin_markup = InlineKeyboardMarkup([[InlineKeyboardButton("✅ قبول", callback_data=f"accept_{user.id}_{order_counter}"), InlineKeyboardButton("❌ رفض", callback_data=f"reject_{user.id}_{order_counter}")]])

    await context.bot.send_photo(chat_id=MY_ADMIN_ID, photo=photo_id, caption=order_text, reply_markup=admin_markup, parse_mode='Markdown')
    await context.bot.send_photo(chat_id=ORDERS_GROUP_ID, photo=photo_id, caption=f"📢 سجل الطلبات:\n{order_text}", parse_mode='Markdown')
    return ConversationHandler.END

# تأكد من إضافة CallbackQueryHandler لمعالجة القبول والرفض

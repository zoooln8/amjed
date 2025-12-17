# --- تعديل دالة طرق الدفع ---
async def get_pay_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    method = update.message.text
    context.user_data['pay_method'] = method
    
    # التحقق إذا ضغط المستخدم إلغاء في هذه المرحلة
    if method == '❌ Cancel':
        return await cancel(update, context)

    if method == 'BOK':
        response = (
            "🏦 **تم اختيار الدفع عبر بنكك (BOK):**\n\n"
            "الرجاء التحويل إلى الحساب التالي:\n"
            "🔢 رقم الحساب: `4923043`\n"
            "👤 الاسم: متجر أمجد للخدمات\n\n"
            "📸 بعد التحويل، يرجى إرسال صورة الإشعار (سكرين شوت) هنا لتأكيد طلبك:"
        )
    elif method == 'My Cashy':
        response = (
            "💸 **تم اختيار الدفع عبر ماي كاشي (My Cashy):**\n\n"
            "الرجاء التحويل إلى الرقم التالي:\n"
            "🔢 الرقم: `401135260`\n\n"
            "📸 بعد إتمام العملية، يرجى إرسال صورة الإشعار هنا:"
        )
    else:
        return ASK_PAY_METHOD # لإجبار المستخدم على اختيار أحد الأزرار

    await update.message.reply_text(response, parse_mode='Markdown')
    return ASK_SCREENSHOT

# --- تحديث الـ ConversationHandler لضمان الاستجابة للإلغاء من أول مرة ---
conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text(['🎮 شحن الألعاب', '💰 الاشتراكات']), select_game_to_order)],
    states={
        ASK_ID: [
            MessageHandler(filters.Text('❌ Cancel'), cancel), # فحص الإلغاء أولاً
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_id)
        ],
        ASK_ITEM: [
            MessageHandler(filters.Text('❌ Cancel'), cancel),
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)
        ],
        ASK_PAY_METHOD: [
            MessageHandler(filters.Text('❌ Cancel'), cancel),
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_pay_method)
        ],
        ASK_SCREENSHOT: [
            MessageHandler(filters.Text('❌ Cancel'), cancel),
            MessageHandler(filters.PHOTO, get_screenshot)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel), MessageHandler(filters.Text('❌ Cancel'), cancel)],
    allow_reentry=True # يسمح ببدء محادثة جديدة فوراً
)

# استخدام نسخة بايثون خفيفة
FROM python:3.9-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المكتبات أولاً للاستفادة من الـ Cache
COPY requirements.txt .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع (الكود)
COPY . .

# أمر تشغيل البوت (تأكد أن اسم ملف الكود هو main.py)
CMD ["python", "main.py"]

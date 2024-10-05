import telebot
import schedule
import time
import json
import random
from threading import Thread

# Load your bot token
TOKEN = 'your-bot-token'
bot = telebot.TeleBot(TOKEN)

# Load data
with open('duaa.json', 'r', encoding='utf-8') as f:
    duaa_data = json.load(f)

with open('adkar.json', 'r', encoding='utf-8') as f:
    adkar_data = json.load(f)

with open('quran.json', 'r', encoding='utf-8') as f:
    quran_data = json.load(f)

# User preferences and scheduled jobs
user_preferences = {}
scheduled_jobs = {}

# Helper functions
def get_detailed_duaa():
    duaa = random.choice(duaa_data)
    content = f"الدعاء:\n"
    for d in duaa['duaa']:
        content += f"{d}\n"
    content += f"\nالفئة: {duaa['category']}\n"
    
    if duaa['source']['quran']:
        content += "\nمصدر القرآن:\n"
        for quran_source in duaa['source']['quran']:
            surah = quran_source['surah']
            ayah = quran_source['ayah']
            content += f"سورة {surah['name']} (رقم {surah['number']}), "
            if ayah['from'] == ayah['to']:
                content += f"الآية {ayah['from']}\n"
            else:
                content += f"الآيات {ayah['from']}-{ayah['to']}\n"
    
    if duaa['source']['hadith']:
        content += "\nمصدر الحديث:\n"
        for hadith in duaa['source']['hadith'][0]:
            content += f"الكتاب: {hadith['book']}\n"
            content += f"الرقم: {hadith['numberOrPage']}\n"
            content += f"الراوي: {hadith['rawi']}\n"
            if hadith['grade']:
                content += f"الدرجة: {hadith['grade']}\n"
    
    return content

def get_detailed_adkar():
    category = random.choice(list(adkar_data.keys()))
    thikr = random.choice(adkar_data[category])
    content = f"الذكر: {thikr['content']}\n\n"
    content += f"الفئة: {category}\n"
    if thikr['count'] != "01":
        content += f"عدد المرات: {thikr['count']}\n"
    if thikr['description']:
        content += f"الوصف: {thikr['description']}\n"
    if thikr['reference']:
        content += f"المرجع: {thikr['reference']}\n"
    return content

def get_detailed_quran():
    verse = random.choice(quran_data)
    content = f"سورة {verse['sura_name_ar']} ({verse['sura_name_en']}) - رقم السورة: {verse['sura_no']}\n"
    content += f"الآية {verse['aya_no']}:\n\n"
    content += f"{verse['aya_text_emlaey']}\n\n"
    content += f"الجزء: {verse['jozz']}\n"
    content += f"الصفحة: {verse['page']}\n"
    content += f"السطر: {verse['line_start']}"
    if verse['line_start'] != verse['line_end']:
        content += f" - {verse['line_end']}"
    return content

def send_message(chat_id, message_type):
    if message_type == 'duaa':
        bot.send_message(chat_id, get_detailed_duaa())
    elif message_type == 'adkar':
        bot.send_message(chat_id, get_detailed_adkar())
    elif message_type == 'quran':
        bot.send_message(chat_id, get_detailed_quran())

# Command handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبا بك! استخدم الأوامر /duaa أو /adkar أو /quran لضبط تفضيلاتك.")

@bot.message_handler(commands=['duaa', 'adkar', 'quran'])
def set_preferences(message):
    chat_id = message.chat.id
    command = message.text.split()[0][1:]  # Remove the '/' from the command
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    markup.add('30 دقيقة', 'ساعة', 'ساعتين', 'مرة في اليوم', 'عشوائي', 'مرتب', 'إيقاف')
    
    bot.send_message(chat_id, f"اختر تفضيلاتك لـ {get_arabic_name(command)}:", reply_markup=markup)
    bot.register_next_step_handler(message, process_preference, command)

def get_arabic_name(command):
    if command == 'duaa':
        return 'الأدعية'
    elif command == 'adkar':
        return 'الأذكار'
    elif command == 'quran':
        return 'القرآن'

def process_preference(message, command):
    chat_id = message.chat.id
    preference = message.text

    if preference == 'إيقاف':
        stop_notifications(chat_id, command)
        bot.send_message(chat_id, f"تم إيقاف إشعارات {get_arabic_name(command)}.")
        return

    if chat_id not in user_preferences:
        user_preferences[chat_id] = {}
    
    user_preferences[chat_id][command] = {
        'frequency': get_frequency(preference),
        'order': 'random' if preference == 'عشوائي' else 'ordered'
    }
    
    schedule_messages(chat_id, command)
    bot.send_message(chat_id, f"تم ضبط تفضيلاتك لـ {get_arabic_name(command)}!")

def get_frequency(preference):
    if preference == '30 دقيقة':
        return '30 minutes'
    elif preference == 'ساعة':
        return '1 hour'
    elif preference == 'ساعتين':
        return '2 hours'
    else:
        return 'once a day'

def schedule_messages(chat_id, message_type):
    pref = user_preferences[chat_id][message_type]
    
    # Cancel any existing job for this chat_id and message_type
    if chat_id in scheduled_jobs and message_type in scheduled_jobs[chat_id]:
        schedule.cancel_job(scheduled_jobs[chat_id][message_type])
    
    if pref['frequency'] == '30 minutes':
        job = schedule.every(30).minutes.do(send_message, chat_id, message_type)
    elif pref['frequency'] == '1 hour':
        job = schedule.every(1).hours.do(send_message, chat_id, message_type)
    elif pref['frequency'] == '2 hours':
        job = schedule.every(2).hours.do(send_message, chat_id, message_type)
    else:  # once a day
        job = schedule.every().day.at("12:00").do(send_message, chat_id, message_type)
    
    if chat_id not in scheduled_jobs:
        scheduled_jobs[chat_id] = {}
    scheduled_jobs[chat_id][message_type] = job

def stop_notifications(chat_id, message_type):
    if chat_id in user_preferences and message_type in user_preferences[chat_id]:
        del user_preferences[chat_id][message_type]
    
    if chat_id in scheduled_jobs and message_type in scheduled_jobs[chat_id]:
        schedule.cancel_job(scheduled_jobs[chat_id][message_type])
        del scheduled_jobs[chat_id][message_type]

# Function to run scheduled tasks
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a separate thread
scheduler_thread = Thread(target=run_scheduler)
scheduler_thread.start()

# Start the bot
bot.polling()
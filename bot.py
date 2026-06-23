API_TOKEN = 'HTTP API:
8827316769:AAHhq3Wwipw4xeLny6IDwS8GUTt3ydxCPdk'
ADMIN_CHAT_ID = 'Id: 8475097494'  # Сюда будут приходить заявки от клиентов

bot = telebot.TeleBot(API_TOKEN)

# Главное меню бота
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('📋 Услуги и цены')
    btn2 = types.KeyboardButton('📍 Адрес и контакты')
    btn3 = types.KeyboardButton('📅 Записаться на визит')
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup

# Старт бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Приветствуем вас в нашей студии! 👋\nЯ бот-помощник. Помогу узнать цены или записаться на визит.",
        reply_markup=main_menu()
    )

# Обработка текстовых кнопок
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == '📋 Услуги и цены':
        services_text = (
            "💰 **Наш прайс-лист:**\n\n"
            "• Комплексный уход — 1 500 руб.\n"
            "• Экспресс-программа — 900 руб.\n"
            "• Премиум сервис — 3 000 руб."
        )
        bot.send_message(message.chat.id, services_text, parse_mode='Markdown')
        
    elif message.text == '📍 Адрес и контакты':
        contacts_text = (
            "🏢 **Мы находимся по адресу:**\n"
            "г. Нижний Новгород, Сормовский район\n\n"
            "📞 **Телефон для связи:** +7 (999) 000-00-00\n"
            "⏰ **Режим работы:** Ежедневно с 10:00 до 21:00"
        )
        bot.send_message(message.chat.id, contacts_text, parse_mode='Markdown')
        
    elif message.text == '📅 Записаться на визит':
        # Переводим пользователя в режим ожидания ввода контактных данных
        msg = bot.send_message(
            message.chat.id, 
            "Пожалуйста, напишите ваше **Имя и Номер телефона**, а также желаемую услугу. "
            "Администратор сразу свяжется с вами!",
            parse_mode='Markdown',
            reply_markup=types.ReplyKeyboardRemove() # Скрываем обычные кнопки
        )
        # Следующее сообщение пользователя будет передано в функцию сохранения заявки
        bot.register_next_step_handler(msg, process_order)

# Функция обработки и пересылки заявки администратору
def process_order(message):
    client_data = message.text
    client_username = f"@{message.from_user.username}" if message.from_user.username else "Не указан"
    
    # Формируем уведомление для владельца бизнеса
    admin_notification = (
        "🚨 **НОВАЯ ЗАЯВКА В БОТЕ!**\n\n"
        f"📝 **Данные от клиента:** {client_data}\n"
        f"👤 **Профиль в TG:** {client_username}"
    )
    
    # Отправляем данные администратору
    bot.send_message(ADMIN_CHAT_ID, admin_notification, parse_mode='Markdown')
    
    # Возвращаем клиента в главное меню
    bot.send_message(
        message.chat.id, 
        "✅ Ваша заявка успешно отправлена администратору! Ожидайте звонка или сообщения.",
        reply_markup=main_menu()
    )

if __name__ == '__main__':
    print("Бот для локального бизнеса успешно запущен...")
    bot.infinity_polling()

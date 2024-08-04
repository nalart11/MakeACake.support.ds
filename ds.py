import disnake
from disnake.ext import commands

# Идентификаторы каналов и ролей
ADMIN_CHANNEL_ID = 0
ADMIN_ROLE_ID = 0

# Токен Discord
TOKEN = 'YOUR_TOKEN'

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Словарь для отслеживания активных диалогов
active_chats = {}

# Словарь переводов
translations = {
    'russian': {
        'choose_language': '🇷🇺 Выберите язык / 🇬🇧 Choose your language / 🇷🇸 Изабери језик',
        'ask_question': '❓ Задайте интересующий вопрос',
        'close_ticket': '🔒 Закрыть тикет',
        'confirm_close_ticket': 'Вы уверены что хотите закрыть тикет?',
        'ticket_closed': 'Тикет закрыт и канал удалён.',
        'private_thread_created': 'Приватная ветка создана. Можете начать диалог.',
        'user_opened_ticket': 'Пользователь {user} открыл тикет.'
    },
    'english': {
        'choose_language': '🇷🇺 Выберите язык / 🇬🇧 Choose your language / 🇷🇸 Изабери језик',
        'ask_question': '❓ Ask a question',
        'close_ticket': '🔒 Close ticket',
        'confirm_close_ticket': 'Are you sure you want to close the ticket?',
        'ticket_closed': 'Ticket closed and channel deleted.',
        'private_thread_created': 'Private thread created. You can start a dialog.',
        'user_opened_ticket': 'User {user} opened a ticket.'
    },
    'serbian': {
        'choose_language': '🇷🇺 Выберите язык / 🇬🇧 Choose your language / 🇷🇸 Изабери језик',
        'ask_question': '❓ Поставите питање',
        'close_ticket': '🔒 Затворите тикет',
        'confirm_close_ticket': 'Да ли сте сигурни да желите да затворите тикет?',
        'ticket_closed': 'Тикет је затворен и канал је обрисан.',
        'private_thread_created': 'Приватна тема је направљена. Можете започети дијалог.',
        'user_opened_ticket': 'Корисник {user} је отворио тикет.'
    }
}

# Команда для запуска бота
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Команда /start
@bot.slash_command(description="Start the bot")
async def start(inter):
    await inter.response.send_message(translations['russian']['choose_language'],
                                      view=LanguageSelectView())

# Класс для меню выбора языка
class LanguageSelectView(disnake.ui.View):
    @disnake.ui.button(label="🇷🇺 Русский", style=disnake.ButtonStyle.primary)
    async def russian_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_main_menu(inter, 'russian')
    
    @disnake.ui.button(label="🇬🇧 English", style=disnake.ButtonStyle.primary)
    async def english_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_main_menu(inter, 'english')
    
    @disnake.ui.button(label="🇷🇸 Српски", style=disnake.ButtonStyle.primary)
    async def serbian_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_main_menu(inter, 'serbian')

# Функции для отправки главного меню
async def send_main_menu(inter, language):
    await inter.response.send_message(translations[language]['ask_question'], view=MainMenuView(language))

# Класс для главного меню
class MainMenuView(disnake.ui.View):
    def __init__(self, language):
        super().__init__()
        self.language = language
        
        labels = self.get_labels(language)
        
        self.who_are_we_button.label = labels['who_are_we']
        self.partnership_button.label = labels['partnership']
        self.how_to_join_button.label = labels['how_to_join']
        self.change_language_button.label = labels['change_language']
        self.contact_us_button.label = labels['contact_us']
    
    @disnake.ui.button(style=disnake.ButtonStyle.secondary, row=0)
    async def who_are_we_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.send_info(inter, "Кто мы такие" if self.language == 'russian' else 
                                     "Who are we" if self.language == 'english' else 
                                     "Ко смо")
    
    @disnake.ui.button(style=disnake.ButtonStyle.secondary, row=1)
    async def partnership_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.send_info(inter, "Партнёрство" if self.language == 'russian' else 
                                     "Partnership" if self.language == 'english' else 
                                     "Партнерство")
    
    @disnake.ui.button(style=disnake.ButtonStyle.secondary, row=2)
    async def how_to_join_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.send_info(inter, "Как к нам попасть" if self.language == 'russian' else 
                                     "How to get to us" if self.language == 'english' else 
                                     "Како доћи до нас")
    
    @disnake.ui.button(style=disnake.ButtonStyle.secondary, row=3)
    async def change_language_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await start(inter)
    
    @disnake.ui.button(style=disnake.ButtonStyle.secondary, row=4)
    async def contact_us_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await start_dialog(inter, self.language)
    
    async def send_info(self, inter, topic):
        if topic == "Кто мы такие":
            await inter.response.send_message("Мы - MakeACake Studios, молодая студия недавно появившаяся практически из ниоткуда. Наш создатель - Великий и Могучий @nalart11, он в принципе руководит всем происходящим здесь.")
        elif topic == "Партнёрство":
            await inter.response.send_message('Для связи с нами вы можете использовать один из нижеперечисленных способов:\n[Наш Discord канал](https://discord.com/invite/uKXcU3py3q)\nНаш ТГ канал (Временно недоступен)\n[ТГ владельца](https://t.me/nalart11)')
        elif topic == "Как к нам попасть":
            await inter.response.send_message('Никак. 💀')
        elif topic == "Who are we":
            await inter.response.send_message("We are MakeACake Studios, a young studio that recently appeared almost out of nowhere. Our creator is the Great and Powerful @nalart11, he basically directs everything that happens here.")
        elif topic == "Partnership":
            await inter.response.send_message('To contact us you can use one of the following methods:\n[Our Discord channel](https://discord.com/invite/uKXcU3py3q)\nOur Telegramm channel (Temporarily unavailable)\n[Owner\'s Telegramm](https://t.me/nalart11)')
        elif topic == "How to get to us":
            await inter.response.send_message('No way. 💀')
        elif topic == "Ко смо":
            await inter.response.send_message("Ми смо MakeACake Studios, млади студио који се недавно појавио готово ниоткуда. Наш креатор је Велики и Моћни @nalart11, он у суштини режира све што се овде дешава.")
        elif topic == "Партнерство":
            await inter.response.send_message('Да бисте нас контактирали, можете користити један од следећих метода:\n[Наш Discord канал](https://discord.com/invite/uKXcU3py3q)\nНаш Telegramm канал (Привремено недоступан)\n[Telegramm за креаторе](https://t.me/nalart11)')
        elif topic == "Како доћи до нас":
            await inter.response.send_message('Не долази у обзир. 💀')

    def get_labels(self, language):
        labels = {}
        if language == 'russian':
            labels = {
                'who_are_we': "Кто мы такие",
                'partnership': "Партнёрство",
                'how_to_join': "Как к нам попасть",
                'change_language': "Изменить язык",
                'contact_us': "Написать нам"
            }
        elif language == 'english':
            labels = {
                'who_are_we': "Who are we",
                'partnership': "Partnership",
                'how_to_join': "How to get to us",
                'change_language': "Change language",
                'contact_us': "Contact us"
            }
        elif language == 'serbian':
            labels = {
                'who_are_we': "Ко смо",
                'partnership': "Партнерство",
                'how_to_join': "Како доћи до нас",
                'change_language': "Промените језик",
                'contact_us': "Контактирајте нас"
            }
        return labels

# Класс для представления кнопки закрытия тикета
class CloseTicketView(disnake.ui.View):
    def __init__(self, language):
        super().__init__()
        self.language = language

    @disnake.ui.button(label="🔒", style=disnake.ButtonStyle.danger)
    async def close_ticket_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_message(translations[self.language]['confirm_close_ticket'], view=ConfirmCloseTicketView(inter.channel, self.language))

class ConfirmCloseTicketView(disnake.ui.View):
    def __init__(self, channel, language):
        super().__init__()
        self.channel = channel
        self.language = language

    @disnake.ui.button(label="🔒", style=disnake.ButtonStyle.danger)
    async def confirm_close_ticket_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.channel.delete()
        await inter.send(translations[self.language]['ticket_closed'])

# Функция для создания приватной ветки
async def start_dialog(inter, language):
    guild = inter.guild
    user = inter.author

    # Проверка, что ADMIN_CHANNEL_ID является категорией
    category = guild.get_channel(ADMIN_CHANNEL_ID)
    if category is None or not isinstance(category, disnake.CategoryChannel):
        await inter.response.send_message("Ошибка: ADMIN_CHANNEL_ID не является категорией или недоступен.")
        return

    # Создание приватной ветки
    overwrites = {
        guild.default_role: disnake.PermissionOverwrite(read_messages=False),
        user: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.get_role(ADMIN_ROLE_ID): disnake.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    
    channel = await guild.create_text_channel(f'private-{user.name}', overwrites=overwrites, category=category)
    
    # Упоминание пользователя и роли администратора
    await channel.send(f"{user.mention} {guild.get_role(ADMIN_ROLE_ID).mention}")
    
    # Удаление сообщения
    last_message = await channel.history(limit=1).flatten()
    if last_message:
        await last_message[0].delete()

    await channel.send(translations[language]['user_opened_ticket'].format(user=user.mention), view=CloseTicketView(language))
    
    await inter.response.send_message(translations[language]['private_thread_created'])

# Запуск бота
bot.run(TOKEN)

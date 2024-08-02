import disnake
import time
from disnake.ext import commands
from datetime import datetime

# Идентификаторы каналов и ролей
ADMIN_CHANNEL_ID = 'Id of cathegory'
ADMIN_ROLE_ID = 'Id of admin role'

# Токен Discord
TOKEN = 'your token'

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Словарь для отслеживания активных диалогов
active_chats = {}

# Команда для запуска бота
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Команда /start
@bot.slash_command(description="Start the bot")
async def start(inter):
    await inter.response.send_message("🇷🇺 Выберите язык / 🇬🇧 Choose your language / 🇷🇸 Изабери језик",
                                      view=LanguageSelectView())

# Класс для меню выбора языка
class LanguageSelectView(disnake.ui.View):
    @disnake.ui.button(label="🇷🇺 Русский", style=disnake.ButtonStyle.primary)
    async def russian_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_russian_main_menu(inter)
    
    @disnake.ui.button(label="🇬🇧 English", style=disnake.ButtonStyle.primary)
    async def english_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_english_main_menu(inter)
    
    @disnake.ui.button(label="🇷🇸 Српски", style=disnake.ButtonStyle.primary)
    async def serbian_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_serbian_main_menu(inter)

# Функции для отправки главного меню
async def send_russian_main_menu(inter):
    await inter.response.send_message('❓ Задайте интересующий вопрос', view=MainMenuView(language='russian'))

async def send_english_main_menu(inter):
    await inter.response.send_message('❓ Ask a question', view=MainMenuView(language='english'))

async def send_serbian_main_menu(inter):
    await inter.response.send_message('❓ Поставите питање', view=MainMenuView(language='serbian'))

# Класс для главного меню
class MainMenuView(disnake.ui.View):
    def __init__(self, language):
        super().__init__()
        self.language = language
    
    @disnake.ui.button(label="Кто мы такие", style=disnake.ButtonStyle.secondary, row=0)
    async def who_are_we(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.send_info(inter, "Кто мы такие")
    
    @disnake.ui.button(label="Партнёрство", style=disnake.ButtonStyle.secondary, row=1)
    async def partnership(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.send_info(inter, "Партнёрство")
    
    @disnake.ui.button(label="Как к нам попасть", style=disnake.ButtonStyle.secondary, row=2)
    async def how_to_join(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.send_info(inter, "Как к нам попасть")
    
    @disnake.ui.button(label="Изменить язык", style=disnake.ButtonStyle.secondary, row=3)
    async def change_language(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await start(inter)
    
    @disnake.ui.button(label="Написать нам", style=disnake.ButtonStyle.secondary, row=4)
    async def contact_us(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await start_dialog(inter)
    
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

# Класс для представления кнопки закрытия тикета
class CloseTicketView(disnake.ui.View):
    def __init__(self):
        super().__init__()

    @disnake.ui.button(label="🔒", style=disnake.ButtonStyle.danger)
    async def close_ticket_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_message("Вы уверены что хотите закрыть тикет?", view=ConfirmCloseTicketView(inter.channel))

class ConfirmCloseTicketView(disnake.ui.View):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    @disnake.ui.button(label="🔒", style=disnake.ButtonStyle.danger)
    async def confirm_close_ticket_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await self.channel.delete()
        await inter.send("Тикет закрыт и канал удалён.")

# Функция для создания приватной ветки
async def start_dialog(inter):
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

    await channel.send(f"Пользователь {user.mention} открыл тикет.", view=CloseTicketView())
    
    await inter.response.send_message("Приватная ветка создана. Можете начать диалог.")

# Запуск бота
bot.run(TOKEN)

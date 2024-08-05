import disnake
from disnake.ext import commands, tasks
from datetime import datetime, timedelta

# Идентификаторы каналов и ролей
ADMIN_CHANNEL_ID = 0
ADMIN_ROLE_ID = 0
MUTE_ROLE_ID = 0

# Токен Discord
TOKEN = 'YOUR_TOKEN'

intents = disnake.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=">", intents=intents)

# Словарь для отслеживания активных диалогов
active_chats = {}
# Список замьюченных каналов
muted_channels = []
# Список замьюченных пользователей
muted_users = {}

# Словарь переводов
translations = {
    'russian': {
        'choose_language': '🇷🇺 Выберите язык / 🇬🇧 Choose your language / 🇷🇸 Изабери језик',
        'ask_question': '❓ Задайте интересующий вопрос',
        'close_ticket': '🔒 Закрыть тикет',
        'confirm_close_ticket': 'Вы уверены что хотите закрыть тикет?',
        'ticket_closed': 'Тикет закрыт и канал удалён.',
        'private_thread_created': 'Приватная ветка создана. Можете начать диалог.',
        'user_opened_ticket': 'Пользователь {user} открыл тикет.',
        'back': 'Назад'
    },
    'english': {
        'choose_language': '🇷🇺 Выберите язык / 🇬🇧 Choose your language / 🇷🇸 Изабери језик',
        'ask_question': '❓ Ask a question',
        'close_ticket': '🔒 Close ticket',
        'confirm_close_ticket': 'Are you sure you want to close the ticket?',
        'ticket_closed': 'Ticket closed and channel deleted.',
        'private_thread_created': 'Private thread created. You can start a dialog.',
        'user_opened_ticket': 'User {user} opened a ticket.',
        'back': 'Back'
    },
    'serbian': {
        'choose_language': '🇷🇺 Выберите язык / 🇬🇧 Choose your language / 🇷🇸 Изабери језик',
        'ask_question': '❓ Поставите питање',
        'close_ticket': '🔒 Затворите тикет',
        'confirm_close_ticket': 'Да ли сте сигурни да желите да затворите тикет?',
        'ticket_closed': 'Тикет је затворен и канал је обрисан.',
        'private_thread_created': 'Приватна тема је направљена. Можете започети дијалог.',
        'user_opened_ticket': 'Корисник {user} је отворио тикет.',
        'back': 'Назад'
    }
}

# Команда для запуска бота
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    unmute_users.start()

# Команда /start
@bot.slash_command(description="Start the bot")
async def start(inter):
    await inter.response.send_message(translations['russian']['choose_language'], view=LanguageSelectView(), ephemeral=True)

# Класс для меню выбора языка
class LanguageSelectView(disnake.ui.View):
    @disnake.ui.button(label="Русский", style=disnake.ButtonStyle.primary)
    async def russian_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_main_menu(inter, 'russian')
    
    @disnake.ui.button(label="English", style=disnake.ButtonStyle.primary)
    async def english_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_main_menu(inter, 'english')
    
    @disnake.ui.button(label="Српски", style=disnake.ButtonStyle.primary)
    async def serbian_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_main_menu(inter, 'serbian')

# Функции для отправки главного меню
async def send_main_menu(inter, language):
    await inter.response.edit_message(content=translations[language]['ask_question'], view=MainMenuView(language))

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
        await inter.response.edit_message(content=translations[self.language]['choose_language'], view=LanguageSelectView())
    
    @disnake.ui.button(style=disnake.ButtonStyle.secondary, row=4)
    async def contact_us_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await start_dialog(inter, self.language)
    
    async def send_info(self, inter, topic):
        if topic == "Кто мы такие":
            await inter.response.edit_message(content="Мы - MakeACake Studios, молодая студия недавно появившаяся практически из ниоткуда. Наш создатель - Великий и Могучий @nalart11, он в принципе руководит всем происходящим здесь.", view=BackToMainMenuView(self.language))
        elif topic == "Партнёрство":
            await inter.response.edit_message(content='Для связи с нами вы можете использовать один из нижеперечисленных способов:\n[Наш Discord канал](https://discord.com/invite/uKXcU3py3q)\nНаш ТГ канал (Временно недоступен)\n[ТГ владельца](https://t.me/nalart11)', view=BackToMainMenuView(self.language))
        elif topic == "Как к нам попасть":
            await inter.response.edit_message(content='Никак. 💀', view=BackToMainMenuView(self.language))
        elif topic == "Who are we":
            await inter.response.edit_message(content="We are MakeACake Studios, a young studio that recently appeared almost out of nowhere. Our creator is the Great and Powerful @nalart11, he basically directs everything that happens here.", view=BackToMainMenuView(self.language))
        elif topic == "Partnership":
            await inter.response.edit_message(content='To contact us you can use one of the following methods:\n[Our Discord channel](https://discord.com/invite/uKXcU3py3q)\nOur Telegramm channel (Temporarily unavailable)\n[Owner\'s Telegramm](https://t.me/nalart11)', view=BackToMainMenuView(self.language))
        elif topic == "How to get to us":
            await inter.response.edit_message(content='No way. 💀', view=BackToMainMenuView(self.language))
        elif topic == "Ко смо":
            await inter.response.edit_message(content="Ми смо MakeACake Studios, млади студио који се недавно појавио готово ниоткуда. Наш креатор је Велики и Моћни @nalart11, он у суштини режира све што се овде дешава.", view=BackToMainMenuView(self.language))
        elif topic == "Партнерство":
            await inter.response.edit_message(content='Да бисте нас контактирали, можете користити један од следећих метода:\n[Наш Discord канал](https://discord.com/invite/uKXcU3py3q)\nНаш Telegramm канал (Привремено недоступан)\n[Telegramm за креаторе](https://t.me/nalart11)', view=BackToMainMenuView(self.language))
        elif topic == "Како доћи до нас":
            await inter.response.edit_message(content='Не долази у обзир. 💀', view=BackToMainMenuView(self.language))

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

# Класс для кнопки "Назад"
class BackToMainMenuView(disnake.ui.View):
    def __init__(self, language):
        super().__init__()
        self.language = language
        self.back_button.label = translations[language]['back']

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.primary)
    async def back_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_main_menu(inter, self.language)

# Класс для представления кнопки закрытия тикета
class CloseTicketView(disnake.ui.View):
    def __init__(self, language):
        super().__init__()
        self.language = language

    @disnake.ui.button(label="🔒", style=disnake.ButtonStyle.danger)
    async def close_ticket_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(content=translations[self.language]['confirm_close_ticket'], view=ConfirmCloseTicketView(inter.channel, self.language))

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
        await inter.response.edit_message(content="Ошибка: ADMIN_CHANNEL_ID не является категорией или недоступен.")
        return

    # Создание приватной ветки
    overwrites = {
        guild.default_role: disnake.PermissionOverwrite(read_messages=False),
        user: disnake.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.get_role(ADMIN_ROLE_ID): disnake.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    
    channel = await guild.create_text_channel(f'private-{user.name}', overwrites=overwrites, category=category)

    await channel.send(translations[language]['user_opened_ticket'].format(user=user.mention), view=CloseTicketView(language))
    
    await inter.response.edit_message(content=translations[language]['private_thread_created'], view=BackToMainMenuView(language))

# Команда /admpan
@bot.slash_command(description="Admin Panel")
async def admpan(inter):
    if ADMIN_ROLE_ID in [role.id for role in inter.author.roles]:
        try:
            await inter.response.send_message(embed=create_admin_panel_embed(), view=AdminPanelView(), ephemeral=True)
        except disnake.Forbidden:
            await inter.response.send_message("Не удалось отправить сообщение в ЛС. Проверьте настройки приватности.", ephemeral=True)
    else:
        await inter.response.send_message("У вас нет прав администратора.", ephemeral=True)

def create_admin_panel_embed():
    return disnake.Embed(
        title="Admin Panel v0.1b0",
        description="Powered by @nalart11\n\nCommands:",
        color=disnake.Color.blue()
    )

class AdminPanelView(disnake.ui.View):
    @disnake.ui.button(label="Mute channel", style=disnake.ButtonStyle.primary)
    async def channel_mute_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_channel_mute_options(inter)
    
    @disnake.ui.button(label="Mute user", style=disnake.ButtonStyle.primary)
    async def user_mute_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await send_user_mute_options(inter)

# Channel Mute
async def send_channel_mute_options(inter):
    embed = disnake.Embed(
        title="Choose option:",
        color=disnake.Color.blue()
    )
    view = ChannelMuteOptionsView()
    await inter.response.edit_message(embed=embed, view=view)

class ChannelMuteOptionsView(disnake.ui.View):
    @disnake.ui.button(label="Mute", style=disnake.ButtonStyle.danger)
    async def mute_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(embed=disnake.Embed(title="Введите ID канала для мута:", color=disnake.Color.blue()), view=ChannelInputView(action="mute"))

    @disnake.ui.button(label="Unmute", style=disnake.ButtonStyle.success)
    async def unmute_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if not muted_channels:
            embed = disnake.Embed(title="No muted channels.", color=disnake.Color.red())
            await inter.response.edit_message(embed=embed, view=BackToMainMenuView())
        else:
            await inter.response.edit_message(embed=disnake.Embed(title="Выберите канал для размьюта:", color=disnake.Color.blue()), view=UnmuteChannelView())

    @disnake.ui.button(label="List", style=disnake.ButtonStyle.secondary)
    async def list_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if not muted_channels:
            embed = disnake.Embed(title="No muted channels.", color=disnake.Color.red())
            await inter.response.edit_message(embed=embed, view=BackToMainMenuView())
        else:
            embed = disnake.Embed(title="Muted channels:", color=disnake.Color.blue())
            for i, channel in enumerate(muted_channels):
                embed.add_field(name=f"{i}. {channel.name}", value=f"<#{channel.id}>", inline=False)
            await inter.response.edit_message(embed=embed, view=BackToMainMenuView())

class ChannelInputView(disnake.ui.View):
    def __init__(self, action):
        super().__init__()
        self.action = action

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(embed=create_admin_panel_embed(), view=AdminPanelView())

    @disnake.ui.button(label="Ввести id канала", style=disnake.ButtonStyle.primary)
    async def submit_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(ChannelIDModal(action=self.action))

class ChannelIDModal(disnake.ui.Modal):
    def __init__(self, action):
        self.action = action
        components = [
            disnake.ui.TextInput(
                label="Channel ID",
                placeholder="Введите ID канала",
                custom_id="channel_id",
                style=disnake.TextInputStyle.short
            )
        ]
        super().__init__(title="Channel ID", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        channel_id = inter.text_values["channel_id"]
        channel_id = int(channel_id)
        channel = inter.guild.get_channel(channel_id)
        if channel is None:
            await inter.response.send_message(embed=disnake.Embed(title="Неверный ID канала.", color=disnake.Color.red()), ephemeral=True)
            return

        if self.action == "mute":
            await mute_channel(inter, channel)
        else:
            await unmute_channel(inter, channel)

async def mute_channel(inter, channel):
    overwrite = channel.overwrites_for(inter.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
    muted_channels.append(channel)
    embed = disnake.Embed(title=f"Канал {channel.name} замьючен.", color=disnake.Color.green())
    await inter.response.send_message(embed=embed, ephemeral=True, view=BackToMainMenuView())

async def unmute_channel(inter, channel):
    overwrite = channel.overwrites_for(inter.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
    muted_channels.remove(channel)
    embed = disnake.Embed(title=f"Канал {channel.name} размьючен.", color=disnake.Color.green())
    await inter.response.send_message(embed=embed, ephemeral=True, view=BackToMainMenuView())

class UnmuteChannelView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        for i, channel in enumerate(muted_channels):
            self.add_item(UnmuteButton(label=f"{channel.name}", custom_id=str(channel.id)))

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(embed=create_admin_panel_embed(), view=AdminPanelView())

class UnmuteButton(disnake.ui.Button):
    def __init__(self, label, custom_id):
        super().__init__(label=label, custom_id=custom_id, style=disnake.ButtonStyle.primary)

    async def callback(self, inter: disnake.MessageInteraction):
        channel_id = int(self.custom_id)
        channel = inter.guild.get_channel(channel_id)
        await unmute_channel(inter, channel)

class BackToMainMenuView(disnake.ui.View):
    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.primary)
    async def back_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(embed=create_admin_panel_embed(), view=AdminPanelView())

# User Mute
async def send_user_mute_options(inter):
    embed = disnake.Embed(
        title="Mute user options:",
        color=disnake.Color.blue()
    )
    view = UserMuteOptionsView()
    await inter.response.edit_message(embed=embed, view=view)

class UserMuteOptionsView(disnake.ui.View):
    @disnake.ui.button(label="Mute user", style=disnake.ButtonStyle.danger)
    async def mute_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(embed=disnake.Embed(title="Введите имя пользователя для мута:", color=disnake.Color.blue()), view=UserInputView(action="mute"))

    @disnake.ui.button(label="Unmute user", style=disnake.ButtonStyle.success)
    async def unmute_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if not muted_users:
            embed = disnake.Embed(title="No muted users.", color=disnake.Color.red())
            await inter.response.edit_message(embed=embed, view=BackToMainMenuView())
        else:
            await inter.response.edit_message(embed=disnake.Embed(title="Выберите пользователя для размьюта:", color=disnake.Color.blue()), view=UnmuteUserView())

class UserInputView(disnake.ui.View):
    def __init__(self, action):
        super().__init__()
        self.action = action

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(embed=create_admin_panel_embed(), view=AdminPanelView())

    @disnake.ui.button(label="Ввести имя пользователя", style=disnake.ButtonStyle.primary)
    async def submit_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.send_modal(UserNameModal(action=self.action))

class UserNameModal(disnake.ui.Modal):
    def __init__(self, action):
        self.action = action
        components = [
            disnake.ui.TextInput(
                label="User Name",
                placeholder="Введите имя пользователя",
                custom_id="user_name",
                style=disnake.TextInputStyle.short
            )
        ]
        super().__init__(title="User Name", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        user_name = inter.text_values["user_name"]
        user = disnake.utils.get(inter.guild.members, name=user_name)
        if user is None:
            await inter.response.send_message(embed=disnake.Embed(title="Неверное имя пользователя.", color=disnake.Color.red()), ephemeral=True)
            return

        if self.action == "mute":
            await select_mute_duration(inter, user)

async def select_mute_duration(inter, user):
    embed = disnake.Embed(
        title="Выберите время мута:",
        color=disnake.Color.blue()
    )
    view = MuteDurationSelectView(user)
    await inter.response.send_message(embed=embed, view=view, ephemeral=True)

class MuteDurationSelectView(disnake.ui.View):
    durations = {
        "60 seconds": 60,
        "5 minutes": 5 * 60,
        "10 minutes": 10 * 60,
        "30 minutes": 30 * 60,
        "1 hour": 60 * 60,
        "3 hours": 3 * 60 * 60,
        "6 hours": 6 * 60 * 60,
        "12 hours": 12 * 60 * 60,
        "24 hours": 24 * 60 * 60,
        "3 days": 3 * 24 * 60 * 60,
        "1 week": 7 * 24 * 60 * 60,
        "1 month": 30 * 24 * 60 * 60,
        "1 year": 365 * 24 * 60 * 60,
        "permanent": None
    }

    def __init__(self, user):
        super().__init__()
        self.user = user
        for label, duration in self.durations.items():
            self.add_item(MuteDurationButton(label=label, duration=duration, user=user))

class MuteDurationButton(disnake.ui.Button):
    def __init__(self, label, duration, user):
        super().__init__(label=label, style=disnake.ButtonStyle.primary)
        self.duration = duration
        self.user = user

    async def callback(self, inter: disnake.MessageInteraction):
        await mute_user(inter, self.user, self.duration)

async def mute_user(inter, user, duration):
    mute_role = inter.guild.get_role(MUTE_ROLE_ID)
    if mute_role is None:
        await inter.response.send_message(embed=disnake.Embed(title="Ошибка: Роль мута не найдена.", color=disnake.Color.red()), ephemeral=True)
        return
    
    await user.add_roles(mute_role)
    if duration:
        unmute_time = datetime.now() + timedelta(seconds=duration)
        muted_users[user.id] = unmute_time
        await inter.response.send_message(embed=disnake.Embed(title=f"Пользователь {user.name} замьючен на {duration} секунд.", color=disnake.Color.green()), ephemeral=True)
    else:
        muted_users[user.id] = None
        await inter.response.send_message(embed=disnake.Embed(title=f"Пользователь {user.name} замьючен навсегда.", color=disnake.Color.green()), ephemeral=True)

# Unmute User
async def send_user_unmute_options(inter):
    embed = disnake.Embed(
        title="Unmute user options:",
        color=disnake.Color.blue()
    )
    view = UnmuteUserView()
    await inter.response.edit_message(embed=embed, view=view)

class UnmuteUserView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        for user_id, unmute_time in muted_users.items():
            user = bot.get_user(user_id)
            if user:
                self.add_item(UnmuteUserButton(label=user.name, user_id=user_id))

    @disnake.ui.button(label="Назад", style=disnake.ButtonStyle.secondary)
    async def back_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.edit_message(embed=create_admin_panel_embed(), view=AdminPanelView())

class UnmuteUserButton(disnake.ui.Button):
    def __init__(self, label, user_id):
        super().__init__(label=label, style=disnake.ButtonStyle.primary)
        self.user_id = user_id

    async def callback(self, inter: disnake.MessageInteraction):
        await unmute_user(inter, self.user_id)

async def unmute_user(inter, user_id):
    guild = inter.guild
    user = guild.get_member(user_id)
    if user:
        mute_role = guild.get_role(MUTE_ROLE_ID)
        if mute_role:
            await user.remove_roles(mute_role)
            del muted_users[user_id]
            await inter.response.send_message(embed=disnake.Embed(title=f"Пользователь {user.name} размьючен.", color=disnake.Color.green()), ephemeral=True)

@tasks.loop(minutes=1)
async def unmute_users():
    now = datetime.now()
    to_unmute = [user_id for user_id, unmute_time in muted_users.items() if unmute_time and unmute_time <= now]
    for user_id in to_unmute:
        guild = bot.get_guild(ADMIN_CHANNEL_ID)
        if guild:
            user = guild.get_member(user_id)
            if user:
                mute_role = guild.get_role(MUTE_ROLE_ID)
                if mute_role:
                    await user.remove_roles(mute_role)
            del muted_users[user_id]

# Запуск бота
bot.run(TOKEN)
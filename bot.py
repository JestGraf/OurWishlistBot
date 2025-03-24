import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

# Вставьте свой токен от BotFather
TOKEN = "8127481993:AAEqIAqn6VrSCXDln8kcM2xZiJvxyouDiWQ"

ADMIN_IDS = {197129326, 1082421881}  # Укажите Telegram ID двух пользователей

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Храним вишлист в памяти (можно заменить на базу данных)
wishlist = []


def get_wishlist_keyboard():
    """Создает клавиатуру с кнопками управления вишлистом."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"{'✅ ' if item['gifted'] else ''}{item['name']}",
                callback_data=f"toggle_{idx}"
            )] for idx, item in enumerate(wishlist)
        ]
    )
    if wishlist:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text="❌ Очистить список", callback_data="clear")
        ])
    return keyboard


@dp.message(Command("start"))
async def start_command(message: Message):
    """Обрабатывает команду /start"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Этот бот предназначен только для двух пользователей.")
        return
    await message.answer("Привет! Это ваш совместный вишлист. Используйте:\n"
                         "/add <ссылка> - добавить подарок\n"
                         "/list - показать вишлист")


@dp.message(Command("add"))
async def add_item(message: Message):
    """Добавляет товар в вишлист"""
    if message.from_user.id not in ADMIN_IDS:
        return
    if len(message.text.split()) < 2:
        await message.answer("Используйте команду в формате: /add <ссылка>")
        return
    link = message.text.split(maxsplit=1)[1]
    wishlist.append({"name": link, "gifted": False})
    await message.answer("✅ Добавлено в вишлист!", reply_markup=get_wishlist_keyboard())


@dp.message(Command("list"))
async def show_wishlist(message: Message):
    """Отображает вишлист"""
    if message.from_user.id not in ADMIN_IDS:
        return
    if not wishlist:
        await message.answer("🎁 Вишлист пуст!")
    else:
        await message.answer("Вот ваш вишлист:", reply_markup=get_wishlist_keyboard())


@dp.callback_query()
async def handle_callback(call: CallbackQuery):
    """Обрабатывает нажатие на кнопки"""
    if call.from_user.id not in ADMIN_IDS:
        return
    if call.data.startswith("toggle_"):
        idx = int(call.data.split("_")[1])
        wishlist[idx]["gifted"] = not wishlist[idx]["gifted"]
        await call.message.edit_reply_markup(reply_markup=get_wishlist_keyboard())
    elif call.data == "clear":
        wishlist.clear()
        await call.message.edit_text("🎁 Вишлист очищен!")


async def main():
    """Запускает бота"""
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())

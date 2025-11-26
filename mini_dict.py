import aiogram
import asyncio
from aiogram import filters, types, F
from langdetect import detect

english_russian_pairs = [
    ["hello", "привет"],
    ["goodbye", "до свидания"],
    ["thank you", "спасибо"],
    ["please", "пожалуйста"],
    ["yes", "да"],
    ["no", "нет"],
    ["friend", "друг"],
    ["family", "семья"],
    ["school", "школа"],
    ["work", "работа"],
    ["city", "город"],
    ["country", "страна"],
    ["food", "еда"],
    ["time", "время"],
    ["day", "день"],
    ["night", "ночь"]
]

token = '...'
bot = aiogram.Bot(token=token)
dp = aiogram.Dispatcher()

def words(values):
    match values:
        case 'EN→RU':
            res = []
            for i in range(0, len(english_russian_pairs)):
                res.append(english_russian_pairs[i][0])
            return res
        
        case 'RU→EN':
            res = []
            for i in range(0, len(english_russian_pairs)):
                res.append(english_russian_pairs[i][1])
            return res


@dp.message(filters.Command('start'))
async def start(message):
    await message.reply('Переводите несколько часто встречающихся слов с английского на русский и обратно.')

@dp.message(filters.Command('langs'))
async def langs(message: types.Message):
    keyboard = [
        [types.InlineKeyboardButton(text = 'EN→RU', callback_data='EN→RU')],
        [types.InlineKeyboardButton(text = 'RU→EN', callback_data='RU→EN')]
    ]
    await message.reply('Поддерживаемые направления:', 
                        reply_markup=types.InlineKeyboardMarkup(inline_keyboard= keyboard))


@dp.callback_query(F.data == 'EN→RU')
async def en_ru_callback(callback: types.CallbackQuery):
    res = words('EN→RU')
    res = '\n'.join(res)

    await callback.message.answer(f'Cписок слов:\n{res}')
    await callback.message.edit_text(
        text = callback.message.text,
        reply_markup=None
    )


@dp.callback_query(F.data == 'RU→EN')
async def en_ru_callback(callback: types.CallbackQuery):    
    res = words('RU→EN')
    res = '\n'.join(res)

    await callback.message.answer(f'Cписок слов:\n{res}')
    await callback.message.edit_text(
        text = callback.message.text,
        reply_markup=None
    )


@dp.message(filters.Command('translate'))
async def translate(message: types.Message, command: filters.CommandObject):
    word = command.args.lower()
    leng = detect(word)
    eng = words('EN→RU')
    ru = words('RU→EN')

    slavic_languages = ['ru', 'uk', 'bg', 'mk', 'sr', 'pl']

    if leng in slavic_languages:
        for i in range(len(ru)):
            if word == ru[i]:
                await message.reply(f"перевод слова {word} - {eng[i]}")
                return
        await message.reply('такого слова нет в словаре, выберите из списка')

    elif word.isascii() and word.isalpha():
        for i in range(len(eng)):
            if word == eng[i]:
                await message.reply(f"перевод слова {word} - {ru[i]}")
                return
        await message.reply('такого слова нет в словаре, выберите из списка')

    else:
        await message.reply('язык не распознан(((')


@dp.message(filters.Command('quick'))
async def reply(message):
    keyboard = [
        [types.KeyboardButton(text = 'hello'), types.KeyboardButton(text = 'yes')],
        [types.KeyboardButton(text = 'друг'), types.KeyboardButton(text = 'семья')],
    ]
    await message.reply('выберите слово для перевода: ',
                        reply_markup=types.ReplyKeyboardMarkup(
                            keyboard = keyboard,
                            resize_keyboard=True
                            )
                        )


@dp.message(filters.Command('actions'))
async def action(message):
    keyboard = [
        [types.InlineKeyboardButton(text='действия для бота', callback_data='show')],
        [types.InlineKeyboardButton(text = 'пожертвование', callback_data='donate')]
    ]
    await message.reply('Что умеет бот?', 
                        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))

@dp.callback_query(F.data == 'show')
async def show(callback: types.CallbackQuery):
    await callback.message.reply(f"команды:\n/quick\n/translate 'слово из списка'\n/langs")

@dp.callback_query(F.data == 'donate')
async def donate(callback: types.CallbackQuery):
    keyboard = [
        [types.InlineKeyboardButton(text='сто миллионов тысяч', callback_data='100')],
        [types.InlineKeyboardButton(text = 'миллионо миллионов', callback_data='1000')]
    ]
    await callback.message.answer(f"донат обязателен, выберите сумму:\n",
                                 reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard))

@dp.callback_query(F.data==('100'))
async def donate_sum(callback: types.CallbackQuery):
    await callback.message.answer('вы задонатили сто миллионов тысяч автору, ему приятно)')

@dp.callback_query(F.data==('1000'))
async def donate_sum(callback: types.CallbackQuery):
    await callback.message.answer('вы задонатили миллионо миллионов автору, ему приятно)')

@dp.message(F.text == 'hello')
async def say_hello(message):
    await message.reply(f"перевод слова hello - привет")

@dp.message(F.text == 'yes')
async def say_yes(message):
    await message.reply(f"перевод слова yes - да")

@dp.message(F.text == 'друг')
async def say_friend(message):
    await message.reply(f"перевод слова друг - friend")

@dp.message(F.text == 'семья')
async def say_family(message):
    await message.reply(f"перевод слова семья - family")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
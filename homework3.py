from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]
],
    resize_keyboard=True)

inline_choices = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
        ]
    ]
)

# # kb = ReplyKeyboardMarkup(resize_keyboard=True)
# # button = KeyboardButton(text='Рассчитать')
# # kb.add(button)
# # button2 = KeyboardButton(text='Информация')
# # kb.add(button2)
# #
# # kb = InlineKeyboardMarkup(resize_keyboard=True)
# # button4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
# # kb.add(button4)
# # button3 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
# # kb.add(button3)
# #
# #
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    # print('Выберите опцию:')
    await message.answer('Выберите опцию:', reply_markup=inline_choices)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    # print('formulas')
    await call.message.answer('10 * вес (кг) + 6,25 * рост (см) - 5 * возраст (г) - 161.')
    await call.answer()


# @dp.message_handler(commands=['start'])
# async def start(message):
#     print('Привет! Я бот помогающий твоему здоровью.')
#     await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    print('Введите свой возраст:')
    await call.message.answer('Введите свой возраст:')
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    print('Введите свой рост:')
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    print('Введите свой вес:')
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    print('Норма каллорий:')
    await state.update_data(weight=message.text)
    date = await state.get_data()
    result = 10 * int(date['weight']) + 6.25 * int(date['growth']) + 4.92 * int(date['age']) - 161
    await message.answer(f"Ваша норма каллорий:{result}")
    await state.finish()

    # @dp.callback_query_handler(text='formulas')
    # async def get_formulas(call):
    #     print('formulas')
    #     await message.answer('10 * int(date['weight']) + 6.25 * int(date['growth']) + 4.92 * int(date['age']) - 161')


@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# @dp.message_handler(text='Рассчитать')
# async def main_menu(message):
#     await message.answer('Выбери опцию:', reply_markup=inline_choices)
#
#
# @dp.callback_query_handler(text="formulas")
# async def get_formulas(call):
#     await call.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
#
#
# @dp.callback_query_handler(text="calories")
# async def set_age(call):
#     await call.message.answer("Введите свой возраст:")
#     await call.answer()
#     await UserState.age.set()
#
#
# @dp.message_handler(state=UserState.age)
# async def set_growth(message, state):
#     await state.update_data(age=message.text)
#     await message.answer("Введите свой рост:")
#     await UserState.growth.set()
#
#
# @dp.message_handler(state=UserState.growth)
# async def set_weight(message, state):
#     await state.update_data(growth=message.text)
#     await message.answer("Введите свой вес:")
#     await UserState.weight.set()
#
#
# @dp.message_handler(state=UserState.weight)
# async def send_calories(message, state):
#     await state.update_data(weight=message.text)
#     data = await state.get_data()
#     result = 10 * int(data['weight']) + 6.25 * int(data['growth']) + 4.92 * int(data['age']) - 161
#     await message.answer(f'Ваша норма калорий {result}')
#     await state.finish()
#
#
# @dp.message_handler(commands=['start'])
# async def start(message):
#     await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=menu)
#
#
# @dp.message_handler()
# async def all_message(message):
#     await message.answer('Введите команду /start, чтобы начать общение.')
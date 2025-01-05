from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup



api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = 'Calories')
async def age_set(message):
    await message.answer('Введите ваш возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def growth_set(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите ваш рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def weigth_set(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите ваш вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    res = ((10 * int(data['weight'])) + (6.25 * int(data['growth'])) - (5 * int(data['age'])) + 5)
    await message.answer(f'Ваша норма калорий {res} в день')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
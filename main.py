from config import token
import db
import grafik
import logging
import get_questions
from aiogram import Bot, Dispatcher, executor, types
logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot)
num_question = 19
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    db.create_user(message.from_user.id)
    main_kb = types.InlineKeyboardMarkup()
    main_kb.add(types.InlineKeyboardButton(text = 'Начать тест',callback_data= 'start_quiz'))
    main_kb.add(types.InlineKeyboardButton(text = 'Подробно про полит.координаты', url='https://ru.wikipedia.org/wiki/Политический_спектр'))
    await message.answer('''Здравствуйте!
Это Telegram-Bot, который был разработан для проведения тестов и опросов.
На данный момент вы можете в нём пройти тест на политическую координату.''',reply_markup=main_kb)
@dp.callback_query_handler(lambda query: query.data == 'start_quiz')
async def quiz_start(callback_query: types.CallbackQuery):
    user_id = callback_query.message.chat.id
    db.db_start_quiz(user_id)
    question = get_questions.get_question(db.get_current_question(user_id))
    answer_kb = types.InlineKeyboardMarkup()
    grafik.create_pic(user_id)
    ans  = question[0] + '\n'
    for variant in range(len(question[1])):
        ans += question[1][variant][0] + '\n'
        answer_kb.add(types.InlineKeyboardButton(text = f'{variant+1} вариант.', callback_data=f'answer_question_{str(question[1][variant][1])}'))
    with open(f'{user_id}.jpg', 'rb') as graf:
        await callback_query.message.answer_photo(graf, caption=ans,reply_markup=answer_kb)
    await callback_query.message.delete()

@dp.callback_query_handler(lambda query: query.data.startswith('answer_question_'))
async def answer_question(callback_query: types.CallbackQuery):
    user_id = callback_query.message.chat.id
    coordinates = callback_query.data.split('_')[-1].strip('[').strip(']').split(',')
    coordinates = list(map(str,coordinates))
    coordinates = ' '.join(coordinates)
    db.change_position(user_id,coordinates)
    grafik.create_pic(user_id)
    db.go_to_next_question(user_id)
    question = db.get_current_question(user_id)
    if question == num_question:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text = 'Показать результаты.', callback_data='give_result'))
        await callback_query.message.answer('Вы завершили тест, нажмите на кнопку, чтобы увидеть результаты.',reply_markup=kb)
        await callback_query.message.delete()
    else:
        question = get_questions.get_question(db.get_current_question(user_id))
        ans = question[0] + '\n'
        answer_kb = types.InlineKeyboardMarkup()
        for variant in range(len(question[1])):
            ans += question[1][variant][0] + '\n'
            answer_kb.add(
                types.InlineKeyboardButton(text=f'{variant+1} вариант.', callback_data=f'answer_question_{str(question[1][variant][1])}'))
        with open(f'{user_id}.jpg','rb') as graf:
            await callback_query.message.answer_photo(graf,caption = ans, reply_markup=answer_kb,)
        await callback_query.message.delete()
@dp.callback_query_handler(lambda query: query.data == 'give_result')
async def results(callback_query: types.CallbackQuery):
    user_id = callback_query.message.chat.id
    grafik.create_pic(user_id)
    with open(f'{user_id}.jpg','rb') as graf:
        a = db.give_results(callback_query.message.chat.id)
        await callback_query.message.answer_photo(graf, caption='Вы успешно завершили прохождение теста!\nВаша координата: '+ str(a[-1].replace(' ', ';')))
    await callback_query.message.delete()
    print(a)
    with open('logs.txt','w') as f:
        f.write(f'{a[0]}   {a[2]}')
if __name__ == '__main__':
    db.start_sheet()
    executor.start_polling(dp, skip_updates=True)
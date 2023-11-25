from aiogram.filters import CommandStart, Command
import copy
from aiogram import types, Bot, F
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from loader import dp, msg_router, callback_router, bot
from random import *
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
global tasks


tasks = []



class Task:
    name = ''
    desc = ''

global taskNow
taskNow = Task()
global requestStatus
requestStatus = 0
global msgid


@msg_router.message(CommandStart())
async def cmd_start_handler(msg: types.Message) -> None:
    await msg.answer(f"Привет, {msg.from_user.first_name}.")
    await msg.answer("Для просмотра управления введи /help")


@msg_router.message(Command("help"))
async def write_help(msg: types.Message):
    await msg.answer("Добавить задачу: /addtask")
    await msg.answer("Просмотреть задачи: /managetask")


@msg_router.message(Command("addtask"))
async def add_task_init(msg: types.Message):
    await msg.answer("Напишите название задачи")
    global requestStatus
    requestStatus = 1


@msg_router.message(Command("managetask"))
async def manage_task(msg: types.Message):
    global tasks
    if len(tasks) > 0:
        builder = InlineKeyboardBuilder()
        for i in range(len(tasks)):
            tasknew = tasks[i]
            print(tasknew.name)
            builder.button(text=f"{tasknew.name}", callback_data="callback1")
        await msg.answer("Сейчас есть следующие задачи:", reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        await msg.answer("Сейчас нет задач")


@msg_router.message()
async def add_task_steps(msg: types.Message):
    global requestStatus
    global taskNow
    if requestStatus == 1:
        taskNow.name = msg.text
        await msg.answer("Напишите описание задачи")
        requestStatus = 2
    elif requestStatus == 2:
        taskNow.desc = msg.text
        msg1 = await msg.answer(f"Задача: {taskNow.name}.\nОписание: {taskNow.desc}.")
        builder = InlineKeyboardBuilder()
        builder.button(text="Да", callback_data="accept_task")
        builder.button(text="Нет", callback_data="reject_task")
        global msgid
        msgid = msg1
        await msg.answer("Вас устраивает это?", reply_markup=builder.as_markup(resize_keyboard=True))


@callback_router.callback_query(F.data == "accept_task")
async def accept_task(callback: types.CallbackQuery):
    global taskNow
    global tasks
    global requestStatus
    tasks.append(copy.deepcopy(taskNow))
    taskNow.name = ''
    taskNow.desc = ''
    requestStatus = 0
    global msgid
    await msgid.delete()
    await callback.message.delete()
    await callback.message.answer("Понял, сохраняю")


@callback_router.callback_query(F.data == "reject_task")
async def reject_task(callback: types.CallbackQuery):
    global taskNow
    global requestStatus
    taskNow.name = ''
    taskNow.desc = ''
    requestStatus = 0
    global msgid
    await msgid.delete()
    await callback.message.delete()
    await callback.message.answer("Понял, отмена")



# @msg_router.message(Command("random_generator"))
# async def reply_build(msg: types.Message):
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Нажми меня", callback_data="random_number")
#     builder.adjust(3)
#     await msg.answer("Кнопка отправки случайного числа:", reply_markup=builder.as_markup(resize_keyboard=True))
#
#
# @callback_router.callback_query(F.data == "random_number")
# async def random_number(callback: types.CallbackQuery):
#     await callback.message.answer(str(randint(1, 10)))
#
#
# @msg_router.message()
# async def echo_handler(msg: types.Message) -> None:
#     try:
#         if msg.text == "Убери клавиатуру":
#             await msg.reply("Понял, убираю", reply_markup=types.ReplyKeyboardRemove())
#         else:
#                 await msg.reply(f"{msg.text}, отлично")
#     except TypeError:
#         await msg.answer("Не понял")
#
#
# @msg_router.message()
# async def message_handler(message: Message) -> None:
#     await message.answer('Hello from my router!')
#


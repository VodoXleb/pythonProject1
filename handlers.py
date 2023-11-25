from aiogram.filters import CommandStart, Command, StateFilter
import copy
from aiogram import types, Bot, F
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from loader import dp, msg_router, callback_router, bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from random import *
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
global tasks


tasks = []


class TaskState(StatesGroup):
    typingName = State()
    typingDesc = State()


class Task:
    name = ''
    desc = ''


@msg_router.message(CommandStart())
async def cmd_start_handler(msg: types.Message) -> None:
    await msg.answer(f"Привет, {msg.from_user.first_name}.")
    await msg.answer("Для просмотра управления введи /help")


@msg_router.message(Command("help"))
async def write_help(msg: types.Message):
    await msg.answer("Добавить задачу: /addtask")
    await msg.answer("Просмотреть задачи: /managetask")


@msg_router.message(Command("addtask"))
async def add_task_init(msg: types.Message, state: FSMContext):
    await msg.answer("Напишите название задачи")
    await state.set_state(TaskState.typingName)


@msg_router.message(Command("managetask"))
async def manage_task(msg: types.Message):
    global tasks
    if len(tasks) > 0:
        builder = InlineKeyboardBuilder()
        for i in range(len(tasks)):
            builder.button(text=f"{tasks[i].name}", callback_data=f"manage/{i}")
        await msg.answer("Сейчас есть следующие задачи:", reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        await msg.answer("Сейчас нет задач")


@msg_router.message(TaskState.typingName)
async def add_task_steps(msg: types.Message, state: FSMContext):
    await state.update_data(taskname=msg.text)
    await msg.answer("Напишите описание задачи")
    await state.set_state(TaskState.typingDesc)


@msg_router.message(TaskState.typingDesc)
async def add_task_steps(msg: types.Message, state: FSMContext):
    await state.update_data(taskdesc=msg.text)
    user_data = await state.get_data()
    msg1 = await msg.answer(f"Задача: {user_data['taskname']}.\nОписание: {user_data['taskdesc']}.")
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="accept_task")
    builder.button(text="Нет", callback_data="reject_task")
    await msg.answer("Вас устраивает это?", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.update_data(msgid=msg1)


@callback_router.callback_query(F.data == "accept_task")
async def accept_task(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    global tasks
    tasknow = Task()
    tasknow.name = user_data['taskname']
    tasknow.desc = user_data['taskdesc']
    tasks.append(copy.deepcopy(tasknow))
    await state.clear()
    await user_data['msgid'].delete()
    await callback.message.delete()


@callback_router.callback_query(F.data == "reject_task")
async def reject_task(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await user_data['msgid'].delete()
    await state.clear()
    await callback.message.delete()


@callback_router.callback_query(F.data.find('manage') != -1)
async def manage_task(callback: types.CallbackQuery, state: FSMContext):
    i = int((callback.data.split('/'))[1])
    global tasks
    builder = InlineKeyboardBuilder()
    builder.button(text="Удалить", callback_data=f"delete/{i}")
    builder.button(text="Не удалять", callback_data="dont delete")
    msgid = await callback.message.answer(f"Задача \n Название: {tasks[i].name} \n Описание: {tasks[i].desc}",
                                          reply_markup=builder.as_markup(resize_keyboard=True))
    await state.update_data(msgid=msgid)


@callback_router.callback_query(F.data.startswith('delete'))
async def reject_task(callback: types.CallbackQuery, state: FSMContext):
    global tasks
    i = int((callback.data.split('/'))[1])
    tasks.pop(i)
    user_data = await state.get_data()
    await user_data['msgid'].delete()


@callback_router.callback_query(F.data == "dont delete")
async def reject_task(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await user_data['msgid'].delete()

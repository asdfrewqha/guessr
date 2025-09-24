import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message
from aiohttp import ClientSession
from core.config import ADMIN_ID, BACKEND_URL
from core.keyboards import inline_miniapp_kbd
from utils.api_dependencies import generate_secure_code, get_access_cookies

from bot import redis

router = Router()

logger = logging.getLogger(__name__)


check_code = State()


@router.message(Command("start"))
async def handle_start(message: Message):
    async with ClientSession() as session:
        await session.post(
            url=f"{BACKEND_URL}/register",
            params={
                "id": message.chat.id,
                "name": message.chat.first_name,
                "username": message.chat.username,
            },
        )
    await message.answer("Открыть МиниПриложение:", reply_markup=inline_miniapp_kbd)


@router.message(Command("code"))
async def make_admin(message: Message, state: FSMContext):
    if str(message.chat.id) == ADMIN_ID:
        await message.answer("Введите код...")
        await state.set_state(check_code)
    else:
        code = generate_secure_code()
        await redis.setex(code, 600, message.user.id)
        await message.answer(f"```{code}```", parse_mode="Markdown")


@router.message(check_code)
async def check_admin_code(message: Message, state: FSMContext):
    code = message.text
    cookies = await get_access_cookies(message.chat.id, message.chat.username, redis)
    user_id = await redis.get(code)
    async with ClientSession(cookies=cookies) as session:
        await session.post(
            url=f"{BACKEND_URL}/set-admin/{user_id}",
        )
    await state.clear()

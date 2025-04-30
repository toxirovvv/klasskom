from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import is_registered, register_user
from texts import DARS_JADVALI, OQITUVCHI, MANZIL

router = Router()

class Register(StatesGroup):
    waiting_for_phone = State()

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    if is_registered(message.from_user.id):
        await message.answer("Assalomu alaykum! Quyidagi menyudan birini tanlang: \n\n yoki savollingizni yozib qoldiring!", reply_markup=main_menu())
    else:
        await message.answer("Iltimos, ro‘yxatdan o‘ting!\n\nMisol: <code>Ali Valiyev, +998901234567</code>")
        await state.set_state(Register.waiting_for_phone)

@router.message(Register.waiting_for_phone)
async def register_handler(message: Message, state: FSMContext):
    try:
        name, phone = message.text.split(",")
        register_user(message.from_user.id, name.strip(), phone.strip())
        await message.answer("✅ Ro‘yxatdan o‘tildi!", reply_markup=main_menu())
        await state.clear()
    except:
        await message.answer("❌ Xatolik! Misol: <code>Ali Valiyev, +998901234567</code>")

@router.message(F.text == "📚 Dars jadvali")
async def jadval_handler(message: Message):
    await message.answer(DARS_JADVALI, parse_mode="HTML")

@router.message(F.text == "👩‍🏫 O‘qituvchi")
async def oqituvchi_handler(message: Message):
    await message.answer(OQITUVCHI, parse_mode="HTML")

@router.message(F.text == "🏫 Manzil")
async def manzil_handler(message: Message):
    await message.answer(MANZIL, parse_mode="HTML")

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Dars jadvali")],
            [KeyboardButton(text="👩‍🏫 O‘qituvchi")],
            [KeyboardButton(text="🏫 Manzil")],
        ],
        resize_keyboard=True
    )

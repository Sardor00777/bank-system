import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7862027641:AAGDTmN-6s5vKA8GmbFUYmYRmL7TinoOrMY"
bot = Bot(token=TOKEN)
dp = Dispatcher()


class MalumotlarBoshqaruvchisi:
    FAYL_NOMI = "bank_malumotlar.json"

    @staticmethod
    def yuklash():
        try:
            with open(MalumotlarBoshqaruvchisi.FAYL_NOMI, "r") as fayl:
                return json.load(fayl)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"mijozlar": []}

    @staticmethod
    def saqlash(malumotlar):
        with open(MalumotlarBoshqaruvchisi.FAYL_NOMI, "w") as fayl:
            json.dump(malumotlar, fayl, indent=4)

menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Mijoz qo'shish")],
        [KeyboardButton(text="Hisob ochish")],
        [KeyboardButton(text="Mijozlarni ko'rish")],
        [KeyboardButton(text="Balansni ko'rish")],
        [KeyboardButton(text="Pul qo'yish"), KeyboardButton(text="Pul yechish")],
        [KeyboardButton(text="Chiqish")]
    ],
    resize_keyboard=True
)
@dp.message()
async def start(message: types.Message):
    if message.text == "/start":
        await message.answer("Assalomu alaykum! Bank tizimi botiga xush kelibsiz!", reply_markup=menu_buttons)
    elif message.text == "Mijoz qo'shish":
        await message.answer("Ismingizni kiriting:")
        dp.message.register(ism_qabul)
    elif message.text == "Hisob ochish":
        await message.answer("Hisob raqamini va boshlang'ich balansni kiriting: (Misol: 12345 100000)")
        dp.message.register(hisob_qabul)
    elif message.text == "Mijozlarni ko'rish":
        await mijozlar_korish(message)
    elif message.text == "Balansni ko'rish":
        await balans_korish(message)
    elif message.text == "Chiqish":
        await message.answer("Botdan chiqish uchun /start buyrug'ini qayta bosing.", reply_markup=menu_buttons)

async def ism_qabul(message: types.Message):
    id_raqam = str(message.chat.id)
    malumotlar = MalumotlarBoshqaruvchisi.yuklash()
    malumotlar["mijozlar"].append({"ism": message.text, "id_raqam": id_raqam, "hisoblar": []})
    MalumotlarBoshqaruvchisi.saqlash(malumotlar)
    await message.answer("✅ Mijoz qo'shildi!", reply_markup=menu_buttons)

async def hisob_qabul(message: types.Message):
    id_raqam = str(message.chat.id)
    malumotlar = MalumotlarBoshqaruvchisi.yuklash()
    try:
        hisob_raqami, balans = message.text.split()
        balans = float(balans)
        mijoz = next((m for m in malumotlar["mijozlar"] if m["id_raqam"] == id_raqam), None)
        if mijoz:
            mijoz["hisoblar"].append({"hisob_raqami": hisob_raqami, "balans": balans})
            MalumotlarBoshqaruvchisi.saqlash(malumotlar)
            await message.answer("✅ Hisob ochildi!", reply_markup=menu_buttons)
        else:
            await message.answer("Siz mijoz sifatida ro'yxatdan o'tmagansiz!", reply_markup=menu_buttons)
    except ValueError:
        await message.answer("Noto‘g‘ri format! Misol: 12345 100000")

async def mijozlar_korish(message: types.Message):
    malumotlar = MalumotlarBoshqaruvchisi.yuklash()
    mijozlar_info = "\n".join([f"{m['ism']} (ID: {m['id_raqam']})" for m in malumotlar["mijozlar"]])
    await message.answer(mijozlar_info if mijozlar_info else "Hech qanday mijoz yo'q!", reply_markup=menu_buttons)

async def balans_korish(message: types.Message):
    id_raqam = str(message.chat.id)
    malumotlar = MalumotlarBoshqaruvchisi.yuklash()
    mijoz = next((m for m in malumotlar["mijozlar"] if m["id_raqam"] == id_raqam), None)
    if mijoz and mijoz["hisoblar"]:
        hisoblar_info = "\n".join([f"Hisob raqami: {h['hisob_raqami']}, Balans: {h['balans']} so'm" for h in mijoz["hisoblar"]])
        await message.answer(hisoblar_info, reply_markup=menu_buttons)
    else:
        await message.answer("Sizda ochilgan hisob yo'q!", reply_markup=menu_buttons)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

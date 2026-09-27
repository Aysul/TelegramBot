from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from forms.user import Base
from aiogram.fsm.context import FSMContext

router = Router()

def start_button():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text="Сделать заказ"), KeyboardButton(text="Выбрать Магазин/Ресторан")],
        [KeyboardButton(text="Промокод"), KeyboardButton(text="Про нас")]
        ],
        resize_keyboard=True
    )
    return keyboard
def returns_buttons():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться", callback_data="return")]
        ]
    )
    return keyboard

@router.callback_query(F.data == "return")
async def return_callback(callback: CallbackQuery):
    await callback.message.answer(
        " Здравствуйте!, добро пожаловать в *Яндекс еда*.\nГотовы сделать ваш заказ?.\n\n\n/list - Список магазинов, ресторанов которые ждут твоего заказа!.\n/promocode - Вводи промокод, и получай скидки на товары.\n/about - узнай о нас многое.", parse_mode="Markdown", 
                         reply_markup=start_button()
    )

    await callback.answer()

@router.message(Command("start", "return"))
@router.message(F.text.lower() == "вернуться")
async def hello(message: Message):
    await message.answer(" Здравствуйте!, добро пожаловать в *Яндекс еда*.\nГотовы сделать ваш заказ?.\n\n\n/list - Список магазинов, ресторанов которые ждут твоего заказа!.\n/promocode - Вводи промокод, и получай скидки на товары.\n/about - узнай о нас многое.", parse_mode="Markdown", 
                         reply_markup=start_button())   

@router.message(Command("list"))
@router.message(F.text.lower() == "выбрать магазин/ресторан")
async def hello(message: Message):
    await message.answer("*Яндекс Лавка* — собственный онлайн-супермаркет сервиса с быстрой доставкой готовой еды и продуктов.\n*Пятёрочка* — популярный продуктовый магазин «у дома» с широким ассортиментом.\n*Перекрёсток* — супермаркет с большим выбором свежих продуктов, готовой кулинарии и деликатесов.\n*Магнит (включая «Магнит Семейный» и «Магнит Косметик»)* — продукты питания, бытовая химия и косметика.\n*Лента (и «Мини Лента»)* — крупные гипермаркеты с товарами на любой вкус от продуктов до текстиля.\n*Ашан* — торговая сеть с возможностью собрать большую корзину по оптовым и розничным ценам.\n*ВкусВилл* — магазин натуральных продуктов для здорового питания.\n*Азбука Вкуса* — супермаркет премиум-класса с редкими продуктами и ресторанной кулинарией.\n*Магнит Косметик / Улыбка радуги* — специализированные магазины косметики, парфюмерии и товаров для ухода за домом.\n*Доктор Столетов / ЕАПТЕКА (и другие партнерские аптеки)* — заказ разрешенных к доставке лекарств, витаминов и медицинских товаров.", parse_mode="Markdown")
    await message.answer("Вернуться в меню", reply_markup=returns_buttons())

@router.message(Command("promocode"))
@router.message(F.text.lower() == "промокод")
async def answer(message: Message):
    await message.answer("Введите промокод(Если он у вас есть) и получите скидки и бонусы к товарам")
    await message.answer("Вернуться в меню", reply_markup=returns_buttons())

@router.message(Command("about"))
@router.message(F.text.lower() == "про нас")
async def answer(message: Message):
    await message.answer("Мы сервис - Яндекс еда")
    await message.answer("Вернуться в меню", reply_markup=returns_buttons())

@router.message(F.text.lower() == "сделать заказ")
async def answer(message: Message, state = FSMContext):
    await message.answer("Назовите свое имя")
    await state.set_state(Base.name)

@router.message(Base.name, F.text)
async def procces_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Прекрасно\n Теперь напишите адрес куда вам доставить")
    await state.set_state(Base.location)

@router.message(Base.location, F.text)
async def procces_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)

    await message.answer("Все ваш заказ принят, и будет доставлен вам в течении 30 минут", reply_markup=returns_buttons())

@router.message()
async def mess(message: Message):
    await message.answer("Готовы сделать заказ?")
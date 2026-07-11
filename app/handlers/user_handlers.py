import logging
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message

import app.keyboards.builders as br
import app.keyboards.inlines as il

import app.requests as rq

logger = logging.getLogger(__name__)

user_router = Router()


class OrderStates(StatesGroup):
    selected_item = State()


@user_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logger.info("Пользователь %s запустил бота (/start)", user_id)

    try:
        user = await rq.return_user(user_id)
        if not user:
            logger.info("Новый пользователь %s зарегистрирован в БД", user_id)
            await rq.create_user(user_id, user_name)
            try:
                await message.delete()
            except Exception as e:
                logger.warning("Не удалось удалить сообщение пользователя %s: %s", user_id, e)

            photo = FSInputFile("venv/images_dir/start.png")
            await message.answer_photo(
                photo=photo,
                caption="Привет, пользователь! Ты попал в наш магазинчик {название} впервые. {желаемое описание}",
                reply_markup=il.main_menu,
            )
        else:
            logger.info("Вернувшийся пользователь %s вошел в систему", user_id)
            try:
                await message.delete()
            except Exception as e:
                logger.warning("Не удалось удалить сообщение пользователя %s: %s", user_id, e)

            photo = FSInputFile("venv/images_dir/start.png")
            await message.answer_photo(
                photo=photo,
                caption="Ого, вы вернулись! Добро пожаловать в магазин {название}",
                reply_markup=il.main_menu,
            )
    except Exception as e:
        logger.error("Критическая ошибка в хэндлере start для пользователя %s: %s", user_id, e, exc_info=True)
        await message.answer("Произошла ошибка при запуске бота. Попробуйте позже.")


@user_router.callback_query(F.data == "main_menu")
async def menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    logger.info("Пользователь %s перешел в главное меню", user_id)

    try:
        try:
            await callback.message.delete()
        except Exception as e:
            logger.warning("Не удалось удалить сообщение в меню для %s: %s", user_id, e)

        photo = FSInputFile("venv/images_dir/start.png")
        await callback.message.answer_photo(photo=photo, caption="Вы в главном меню!", reply_markup=il.main_menu)
    except Exception as e:
        logger.error("Ошибка отображения меню с фото для %s: %s. Пробуем текст.", user_id, e)
        await callback.message.answer("Вы в главном меню!", reply_markup=il.main_menu)
    await callback.answer()


@user_router.callback_query(F.data == "feedbacks")
async def callbacks(callback: CallbackQuery):
    logger.info("Пользователь %s нажал кнопку отзывов", callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer("Пожалуйста, оставьте отзыв)", reply_markup=il.feedbacks)
    await callback.answer()


@user_router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info("Пользователь %s запросил профиль", user_id)
    
    try:
        user = await rq.return_user(user_id)

        try:
            await callback.message.delete()
        except Exception as e:
            logger.warning("Не удалось удалить сообщение при открытии профиля %s: %s", user_id, e)

        photo = FSInputFile("images_dir/start.png")
        await callback.message.answer_photo(
            photo=photo,
            caption=f"Ваш профиль:\nИмя: {user.name}\nКоличество заказов: {user.count_of_orders}\nНакопленные баллы: {user.payment_score}",
            reply_markup=il.profile_menu,
        )
    except Exception as e:
        logger.error("Ошибка при генерации профиля для %s: %s", user_id, e, exc_info=True)
        await callback.message.answer(
            f"Ваш профиль:\nИмя: {user.name}\nКоличество заказов: {user.count_of_orders}\nНакопленные баллы: {user.payment_score}",
            reply_markup=il.profile_menu,
        )
    finally:
        await callback.answer()


@user_router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    user_id = callback.from_user.id
    logger.info("Пользователь %s открыл каталог категорий", user_id)
    try:
        await callback.message.delete()
    except Exception as e:
        logger.warning("Не удалось удалить сообщение перед каталогом для %s: %s", user_id, e)

    await callback.message.answer("Выберите желаемую категорию товаров:", reply_markup=await br.inline_categories())
    await callback.answer()


@user_router.callback_query(lambda call: "category" in call.data)
async def selected_category(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        category_id = callback.data.split("category")[1]
        if category_id:
            category_id = int(category_id)
            await state.set_state(OrderStates.selected_item)
            logger.info("Пользователь %s выбрал ID категории: %s", user_id, category_id)
        
            category = await rq.return_category(category_id)

            if not category:
                logger.warning("Пользователь %s выбрал несуществующую категорию %s", user_id, category_id)
                await callback.answer("Категория не найдена.", show_alert=True)
                return

            category_name = category.name
            await state.update_data(category_id=category_id, category_name=category_name)

            try:
                await callback.message.delete()
            except Exception as e:
                logger.warning("Не удалось удалить сообщение в категории для %s: %s", user_id, e)

        
        else:
            logger.info("Пользователь %s вернулся из карточки товара к другим товарам: %s", user_id, category_id)
            category = await state.get_data()

            if not category:
                logger.warning("Пользователь %s выбрал несуществующую категорию %s", user_id, category_id)
                await callback.answer("Категория не найдена.", show_alert=True)
                return

            category_name = category.get("category_name")
            category_id = category.get("category_id")

            try:
                await callback.message.delete()
            except Exception as e:
                logger.warning("Не удалось удалить сообщение в категории для %s: %s", user_id, e)

        await callback.message.answer(f"Выберите товар из выбранной вами категории: {category_name}", reply_markup=await br.inline_items(category_id))

    except (IndexError, ValueError) as e:
        logger.error("Ошибка парсинга категории из callback.data (%s) пользователем %s: %s", callback.data, user_id, e)
        await callback.answer("Ошибка при выборе категории.", show_alert=True)

    except Exception as e:
        logger.error("Непредвиденная ошибка в selected_category для %s: %s", user_id, e, exc_info=True)
        await callback.answer("Произошла непредвиденная ошибка.")

    finally:
        await callback.answer()


@user_router.callback_query(lambda call: "item" in call.data)
async def selected_item(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    if "item" in callback.data:
        try:
            item_id = int(callback.data.split("item")[1])
            logger.info("Пользователь %s выбрал товар ID: %s", user_id, item_id)
            await state.update_data(item_id=item_id, item_amount=1)

        except (IndexError, ValueError) as e:
            logger.error("Ошибка парсинга товара из %s пользователем %s: %s", callback.data, user_id, e)
            await callback.answer("Ошибка обработки товара.", show_alert=True)
            return

    item_data = await state.get_data()
    item_id = item_data.get("item_id")
    item_amount = item_data.get("item_amount", 1)
    category_name = item_data.get("category_name", "Не указана")

    if not item_id:
        logger.warning("У пользователя %s устарела сессия (отсутствует item_id)", user_id)
        await callback.answer("Сессия устарела. Пожалуйста, выберите товар заново.", show_alert=True)
        return

    try:
        item = rq.return_item(item_id)
        if not item:
            logger.warning("Товар ID %s не найден в БД при запросе от %s", item_id, user_id)
            await callback.answer("Товар не найден в базе данных.", show_alert=True)
            return

        item_name = item.name
        item_price = item.price

        text = f"Вы выбрали:\nКатегория: {category_name}\nТовар: {item_name}\nСтоимость: {item_price}₽\nКоличество: {item_amount}"

        if callback.message.photo:
            try:
                await callback.message.delete()

            except Exception as e:
                logger.warning("Не удалось удалить сообщение с фото для %s: %s", user_id, e)

            await callback.message.answer(text=text, reply_markup=il.selected_item)

        else:
            try:
                await callback.message.edit_text(text=text, reply_markup=il.selected_item)

            except Exception as e:
                logger.warning("Не удалось отредактировать текст для %s (%s). Шлем новое сообщение.", user_id, e)
                await callback.message.answer(text=text, reply_markup=il.selected_item)

    except Exception as e:
        logger.error("Ошибка получения данных о товаре %s для %s: %s", item_id, user_id, e, exc_info=True)
        await callback.answer("Ошибка получения данных о товаре.")

    finally:
            await callback.answer()

@user_router.callback_query(F.data.in_(["plus_amount", "minus_amount"]))
async def change_amount(callback: CallbackQuery, state: FSMContext):
    item_data = await state.get_data()
    item_amount = item_data.get("item_amount", 1)
    user_id = callback.from_user.id
    
    if callback.data == "plus_amount":
        logger.info("Пользователь %s увеличивает количество (было: %s)", user_id, item_amount)
        await state.update_data(item_amount=item_amount + 1)

    else:
        if item_amount - 1 != 0:
            logger.info("Пользователь %s уменьшает количество (было: %s)", user_id, item_amount)
            await state.update_data(item_amount=item_amount - 1)

        else:
            logger.warning("Пользователь %s попытался опустить количество ниже 1", user_id)
            await callback.answer("Недопустимое количество товара!", show_alert=True)
            return

    await selected_item(callback, state)

@user_router.callback_query(F.data == "buy")
async def buying_item(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    item_data = await state.get_data()



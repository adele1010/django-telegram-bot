import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from main.models import Product  # Импорт модели

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команда для просмотра всех товаров
async def list_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    products = Product.objects.all()
    if products.exists():
        response = "\n".join([f"{p.name}: {p.price} ₽" for p in products])
    else:
        response = "Список товаров пуст."
    await update.message.reply_text(response)

# Команда для добавления нового товара
async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Используйте: /add_product <название> <цена>")
        return

    name = context.args[0]
    price = context.args[1]
    try:
        price = float(price)
        Product.objects.create(name=name, price=price)
        await update.message.reply_text(f"Товар '{name}' добавлен!")
    except ValueError:
        await update.message.reply_text("Цена должна быть числом.")

# Основная функция
async def main():
    application = ApplicationBuilder().token("7672688450:AAH0-8gU8r-MJ3Fp2nRn-mnJTMVZYE5jJpI").build()

    application.add_handler(CommandHandler("list_products", list_products))
    application.add_handler(CommandHandler("add_product", add_product))

    await application.run_polling()

if __name__ == '__main__':
    import django
    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    import asyncio
    asyncio.run(main())

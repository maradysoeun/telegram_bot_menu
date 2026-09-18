
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

foods = {
    "burger": {
        "name": "Burger",
        "price": 3.50
    },
    "pizza": {
        "name": "Pizza",
        "price": 5.00
    },
    "fried_rice": {
        "name": "Fried Rice",
        "price": 3.00
    },
    "fried_noodle": {
        "name": "Fried Noodle",
        "price": 3.00
    },
    "coke": {
        "name": "Coca Cola",
        "price": 1.00
    },
    "water": {
        "name": "Water",
        "price": 0.50
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    button1 = InlineKeyboardButton("🍔 Food Menu", callback_data="menu")
    button2 = InlineKeyboardButton("🛒 My Order", callback_data="cart")

    keyboard = [
        [button1],
        [button2]
    ]

    reply = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome to our restaurant! 🍴\n\n"
        "Please choose an option:",
        reply_markup=reply
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    button1 = InlineKeyboardButton("🍔 Main Food", callback_data="main")
    button2 = InlineKeyboardButton("🥤 Drinks", callback_data="drinks")
    button3 = InlineKeyboardButton("🛒 My Order", callback_data="cart")

    keyboard = [
        [button1],
        [button2],
        [button3]
    ]

    reply = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "🍴 FOOD MENU\n\n"
        "Choose a category:",
        reply_markup=reply
    )


async def main_food(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    button1 = InlineKeyboardButton(
        "🍔 Burger - $3.50",
        callback_data="food_burger"
    )

    button2 = InlineKeyboardButton(
        "🍕 Pizza - $5.00",
        callback_data="food_pizza"
    )

    button3 = InlineKeyboardButton(
        "🍚 Fried Rice - $3.00",
        callback_data="food_fried_rice"
    )

    button4 = InlineKeyboardButton(
        "🍜 Fried Noodle - $3.00",
        callback_data="food_fried_noodle"
    )

    button5 = InlineKeyboardButton(
        "⬅️ Back",
        callback_data="menu"
    )

    keyboard = [
        [button1],
        [button2],
        [button3],
        [button4],
        [button5]
    ]

    reply = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "🍴 MAIN FOOD\n\n"
        "Choose your food:",
        reply_markup=reply
    )


async def drinks(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    button1 = InlineKeyboardButton(
        "🥤 Coca Cola - $1.00",
        callback_data="food_coke"
    )

    button2 = InlineKeyboardButton(
        "💧 Water - $0.50",
        callback_data="food_water"
    )

    button3 = InlineKeyboardButton(
        "⬅️ Back",
        callback_data="menu"
    )

    keyboard = [
        [button1],
        [button2],
        [button3]
    ]

    reply = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "🥤 DRINKS\n\n"
        "Choose your drink:",
        reply_markup=reply
    )


async def food(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    food_id = query.data.replace("food_", "")

    name = foods[food_id]["name"]
    price = foods[food_id]["price"]

    button1 = InlineKeyboardButton(
        "➕ Add to Order",
        callback_data="add_" + food_id
    )

    button2 = InlineKeyboardButton(
        "🛒 My Order",
        callback_data="cart"
    )

    button3 = InlineKeyboardButton(
        "⬅️ Back",
        callback_data="menu"
    )

    keyboard = [
        [button1],
        [button2],
        [button3]
    ]

    reply = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "🍴 " + name + "\n\n"
        "💰 Price: $" + str(price) + "\n\n"
        "Would you like to add this to your order?",
        reply_markup=reply
    )


async def add_food(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer("Added to your order!")

    food_id = query.data.replace("add_", "")

    if "cart" not in context.user_data:
        context.user_data["cart"] = {}

    cart = context.user_data["cart"]

    if food_id in cart:
        cart[food_id] = cart[food_id] + 1
    else:
        cart[food_id] = 1

    button1 = InlineKeyboardButton(
        "➕ Add Again",
        callback_data="add_" + food_id
    )

    button2 = InlineKeyboardButton(
        "🛒 My Order",
        callback_data="cart"
    )

    button3 = InlineKeyboardButton(
        "🍴 Food Menu",
        callback_data="menu"
    )

    keyboard = [
        [button1],
        [button2],
        [button3]
    ]

    reply = InlineKeyboardMarkup(keyboard)

    name = foods[food_id]["name"]

    await query.edit_message_text(
        "✅ " + name + " added to your order!\n\n"
        "Quantity: " + str(cart[food_id]),
        reply_markup=reply
    )


async def cart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if "cart" not in context.user_data:
        context.user_data["cart"] = {}

    cart = context.user_data["cart"]

    if len(cart) == 0:

        button = InlineKeyboardButton(
            "🍴 Food Menu",
            callback_data="menu"
        )

        keyboard = [[button]]

        reply = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "🛒 Your order is empty.",
            reply_markup=reply
        )

        return

    message = "🛒 YOUR ORDER\n\n"

    total = 0

    for food_id in cart:

        quantity = cart[food_id]

        name = foods[food_id]["name"]
        price = foods[food_id]["price"]

        subtotal = price * quantity

        total = total + subtotal

        message = message + (
            name + "\n"
            + str(quantity) + " x $"
            + str(price)
            + " = $"
            + str(subtotal)
            + "\n\n"
        )

    message = message + "💰 Total: $" + str(round(total, 2))

    button1 = InlineKeyboardButton(
        "📦 Place Order",
        callback_data="checkout"
    )

    button2 = InlineKeyboardButton(
        "🗑 Clear Order",
        callback_data="clear"
    )

    button3 = InlineKeyboardButton(
        "🍴 Food Menu",
        callback_data="menu"
    )

    keyboard = [
        [button1],
        [button2],
        [button3]
    ]

    reply = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        message,
        reply_markup=reply
    )


async def clear_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    context.user_data["cart"] = {}

    button = InlineKeyboardButton(
        "🍴 Food Menu",
        callback_data="menu"
    )

    keyboard = [[button]]

    reply = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "🗑 Your order has been cleared.",
        reply_markup=reply
    )


async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    cart = context.user_data.get("cart", {})

    if len(cart) == 0:
        await query.edit_message_text(
            "Your order is empty."
        )
        return

    message = "📦 NEW ORDER\n\n"

    total = 0

    for food_id in cart:

        quantity = cart[food_id]

        name = foods[food_id]["name"]
        price = foods[food_id]["price"]

        subtotal = price * quantity

        total = total + subtotal

        message = message + (
            name + "\n"
            + "Quantity: " + str(quantity) + "\n"
            + "Price: $" + str(subtotal)
            + "\n\n"
        )

    user = query.from_user

    message = message + (
        "💰 Total: $" + str(round(total, 2)) + "\n\n"
        "👤 Customer: " + user.full_name + "\n"
        "🆔 Telegram ID: " + str(user.id)
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=message
    )

    context.user_data["cart"] = {}

    await query.edit_message_text(
        "✅ ORDER RECEIVED!\n\n"
        "Thank you for your order! 🍴\n"
        "The restaurant has received your order."
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if query.data == "menu":
        await menu(update, context)

    elif query.data == "main":
        await main_food(update, context)

    elif query.data == "drinks":
        await drinks(update, context)

    elif query.data.startswith("food_"):
        await food(update, context)

    elif query.data.startswith("add_"):
        await add_food(update, context)

    elif query.data == "cart":
        await cart(update, context)

    elif query.data == "clear":
        await clear_cart(update, context)

    elif query.data == "checkout":
        await checkout(update, context)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot is running...")

app.run_polling()


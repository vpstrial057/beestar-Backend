import os
from dotenv import load_dotenv
import telebot
from telebot import types

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    print("Bot token is not defined. Please check your environment variables.")
else:
    print("Bot token is loaded properly.")

bot = telebot.TeleBot(TOKEN)


# Define the guide text
guide_text = (
    "How to play Beestar Kombat 🐝\n\n"
    # "Full version of the guide: (https://beestar-kombat.notion.site/Beestar-Kombat-manual-7e53c342eef143de8bc9c8262ea3a36d)\n\n"
    "💰 Tap to earn\n"
    "Tap the screen and collect honey.\n\n"
    "⛏ Harvest\n"
    "Upgrade hives that will give you passive income opportunities.\n\n"
    "⏰ Profit per hour\n"
    "The hive will produce honey for you on its own, even when you are not in the game for 3 hours. "
    "Then you need to log in to the game again.\n\n"
    "📈 LVL\n"
    "The more honey you have on your balance, the higher the level of your hive is and the faster you can earn more honey.\n\n"
    "👥 Friends\n"
    "Invite your fellow bees and you’ll get bonuses. Help a friend move to the next hive leagues and you'll get even more bonuses.\n\n"
    "🪙 Token listing\n"
    "At the end of the season, a honeycomb token will be released and distributed among the players. "
    "Dates will be announced in our announcement channel. Stay tuned!\n\n"
    "/help to get this guide"
)


def create_markup(include_guide_button=True, user_name=None, user_id=None):
    """Creates the inline keyboard markup with play, guide, and group buttons."""
    markup = types.InlineKeyboardMarkup()
    game_url = f"https://beestar-kombat-omega.vercel.app/?id={user_id}&userName={user_name}"
    print("backend bot",game_url)
    play_button = types.InlineKeyboardButton(
        text="Click to play 🎮", web_app=types.WebAppInfo(game_url)
    )
    group_button = types.InlineKeyboardButton(
        text="Join our Telegram group 📢", url="https://t.me/BTFannouncement"
    )
    markup.add(play_button)
    if include_guide_button:
        guide_button = types.InlineKeyboardButton(
            text="How to earn money 💰", callback_data="guide"
        )
        markup.add(guide_button)
    markup.add(group_button)
    return markup


# Start Bot
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_name = message.chat.first_name
    user_id = message.chat.id
    print("user",user_name, user_id)
    message_text = (
        f"Hello {user_name}! Welcome to Beestar Kombat 🐝\n"
        "You are now the director of a buzzing exchange. Which one? You choose. \n\n"
        "Tap the hive, collect honey, boost your passive income, and develop your own honey-making strategy.\n"
        "Your efforts will be appreciated once the honeycomb tokens are listed (the date is coming soon).\n"
        "Don't forget your fellow bees — bring them into the game and collect even more honey together!"
    )

    markup = create_markup(user_name=user_name, user_id=user_id)
    bot.send_message(message.chat.id, message_text, reply_markup=markup)


@bot.message_handler(commands=["help"])
def send_help(message):
    markup = create_markup(include_guide_button=False, user_name=message.chat.first_name, user_id=message.chat.id)
    bot.send_message(message.chat.id, guide_text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "guide")
def show_guide(call):
    bot.answer_callback_query(call.id)
    markup = create_markup(include_guide_button=False, user_name=call.from_user.first_name, user_id=call.from_user.id)
    bot.send_message(call.message.chat.id, guide_text, reply_markup=markup)


bot.polling(none_stop=True)

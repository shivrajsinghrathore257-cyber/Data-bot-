import telebot
import time
import threading
from flask import Flask

# --- Render ke liye Flask Server (Zaruri Hai) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Active 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- Bot Configuration ---
BOT_TOKEN = "8667049229:AAHL-Q-dXudxIYOFtgawcvGmDIKrGg22KM8" # <--- Apna Token Yaha Dalein
bot = telebot.TeleBot(BOT_TOKEN)

# Links
OFFER_LINK = "https://shivrajsinghrathore257-cyber.github.io/Vip-offer/"
RACE_LINK = "https://www.hvqzf09xs80rl27.com/#/register?invitationCode=32775781092"
CONTACT_MSG = "📢 PURI DETAILS KE LIYE MESSAGE KRE\n👤 @SR_NOTES8"

# User Tracking (Note: Server restart hone par ye reset ho jayega)
used_users = set()

# Deletion Function
def delete_msg(chat_id, msg_id, delay):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, msg_id)
    except:
        pass

# --- Start Command Logic ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    
    if user_id in used_users:
        bot.send_message(user_id, "❌ आपको लिंक पहले ही भेजा जा चुका है!")
        return

    used_users.add(user_id)
    
    # 1. Contact Message
    bot.send_message(user_id, CONTACT_MSG)
    
    # 2. 1 Second Gap
    time.sleep(1)
    
    # 3. Offer Link Message
    link_text = f"CLICK HERE 🔗 {OFFER_LINK}"
    msg = bot.send_message(user_id, link_text)
    
    # 4. 62 Seconds Deletion
    threading.Thread(target=delete_msg, args=(user_id, msg.message_id, 62)).start()

# --- Hidden Commands ---
@bot.message_handler(commands=['chiku'])
def handle_chiku(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, f"🚀 VIP OFFER:\n{OFFER_LINK}")
    threading.Thread(target=delete_msg, args=(user_id, msg.message_id, 60)).start()

@bot.message_handler(commands=['race'])
def handle_race(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, f"🏁 REGISTRATION:\n{RACE_LINK}")
    threading.Thread(target=delete_msg, args=(user_id, msg.message_id, 5)).start()

# --- Execution ---
if __name__ == "__main__":
    # Flask ko alag thread mein chalao
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    print("🤖 Bot is starting on Render...")
    bot.infinity_polling()

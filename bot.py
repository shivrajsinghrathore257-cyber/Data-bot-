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
BOT_TOKEN = "8667049229:AAHL-Q-dXudxIYOFtgawcvGmDIKrGg22KM8"
bot = telebot.TeleBot(BOT_TOKEN)

# Links
OFFER_LINK = "https://shivrajsinghrathore257-cyber.github.io/Vip-offer/"
RACE_LINK = "https://www.hvqzf09xs80rl27.com/#/register?invitationCode=32775781092"

# User Tracking
used_users = set()

# Deletion Function
def delete_msg(chat_id, msg_id, delay):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, msg_id)
        print(f"✅ Deleted message {msg_id}")
    except:
        pass

# Permanent Message Formatting
PERMANENT_MSG = """<b>📢 हमारे चैनल में हम ज्यादा members नहीं रखते!</b>

<b>हम सिर्फ 50 लोगों को ही select करेंगे।</b>

<b>सभी मिलकर analysis करेंगे कि आगे क्या आने वाला है.</b>

<b>✅ FREE TRIAL USE करना है तो:</b> <b>YES मैसेज करें</b>

👤 संपर्क: @SR_NOTES8"""

# --- Start Command ---
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    
    if user_id in used_users:
        bot.send_message(user_id, "❌ आपको लिंक पहले ही भेजा जा चुका है!")
        return

    used_users.add(user_id)
    
    # 1. Permanent Message
    bot.send_message(user_id, PERMANENT_MSG, parse_mode='HTML')
    time.sleep(1)
    
    # 2. Expiring Link Message
    link_text = f"<b>🔥 VIP OFFER 🔥</b>\n\n👉 {OFFER_LINK}\n\n<i>⚠️ यह लिंक 62 सेकंड में गायब हो जाएगा!</i>"
    msg = bot.send_message(user_id, link_text, parse_mode='HTML')
    
    t = threading.Thread(target=delete_msg, args=(user_id, msg.message_id, 62))
    t.daemon = True
    t.start()

# --- Hidden Commands ---
@bot.message_handler(commands=['chiku'])
def handle_chiku(message):
    user_id = message.chat.id
    link_text = f"<b>🚀 VIP OFFER</b>\n\n👉 {OFFER_LINK}\n\n<i>⚠️ यह लिंक 62 सेकंड में गायब हो जाएगा!</i>"
    msg = bot.send_message(user_id, link_text, parse_mode='HTML')
    
    t = threading.Thread(target=delete_msg, args=(user_id, msg.message_id, 62))
    t.daemon = True
    t.start()

@bot.message_handler(commands=['race'])
def handle_race(message):
    user_id = message.chat.id
    msg = bot.send_message(user_id, f"🏁 <b>REGISTRATION LINK</b>\n\n👉 {RACE_LINK}", parse_mode='HTML')
    
    t = threading.Thread(target=delete_msg, args=(user_id, msg.message_id, 5))
    t.daemon = True
    t.start()

# --- Execution ---
if __name__ == "__main__":
    # Flask ko alag thread mein chalao taaki Render active rahe
    t_flask = threading.Thread(target=run_flask)
    t_flask.daemon = True
    t_flask.start()
    
    print("🤖 Bot is starting on GitHub/Render...")
    bot.infinity_polling()

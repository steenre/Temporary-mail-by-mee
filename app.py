from flask import Flask
from threading import Thread
import telebot
import requests
import json
import os

app = Flask(__name__)
bot = telebot.TeleBot('7818501334:AAHtroDr-CgOuwGexDGhMJI9aAtJ55pAjSU')
admin = "OWNER USED ID"

#
def file_exists(file_path):
    return os.path.exists(file_path)

#
    if not os.path.exists("admin"):
      os.makedirs("admin")

#
    total_file = "admin/mail.txt"
    if not os.path.exists(total_file):
      with open(total_file, 'w') as f:
          f.write("0")




if not os.path.exists("admin"):
    os.makedirs("admin")

#
total_file = "admin/total.txt"
if not os.path.exists(total_file):
    with open(total_file, 'w') as f:
        f.write("0")

total_file = "admin/mail.txt"
if not os.path.exists(total_file):
    with open(total_file, 'w') as f:
        f.write("0")

#
total_file = "admin/total.txt"
if not os.path.exists(total_file):
    with open(total_file, 'w') as f:
        f.write("0")


#
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    fname = message.from_user.first_name
    lname = message.from_user.last_name
    ulogin = message.from_user.username
#
    users_directory = "admin/users/"
    if not os.path.exists(users_directory):
        os.makedirs(users_directory)

    if not file_exists(f"{users_directory}{user_id}.json"):
        bot.send_message(admin, f"<b>🚀 New User Joined The Bot\n\nUser Id : {user_id}\n\nFirst Name: {fname}\n\nLast name: {lname}</b>")
        open(f"{users_directory}{user_id}.json", "w").close()
#
    mess = f"<b>😀 Hey {fname} Welcome To the @{bot.get_me().username}\n\nBot Created By : @developerke</b>"
    keyboard_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    keyboard_markup.row("🚀 My Email")
    keyboard_markup.row("📧 Generate New Email", "📨 Inbox")
    keyboard_markup.row("📊  Status")
    bot.send_message(user_id, mess, reply_markup=keyboard_markup, parse_mode='HTML')



#
@bot.message_handler(func=lambda message: message.text == '📧 Generate New Email')
def generate_email(message):
    user_id = message.from_user.id

    url = "https://api.internal.temp-mail.io/api/v3/email/new"
    headers = {"Content-Type": "application/json"}
    data = {"min_name_length": 10, "max_name_length": 10}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        email = response.json()['email']
        bot.send_message(user_id, f"<b>Your Email Successfully Generated\n{email}</b>", parse_mode='HTML')
        with open(f"admin/mail{user_id}.json", "w") as mail_file:
            mail_file.write(json.dumps({"email": email}))
        h = int(open("admin/mail.txt").read()) + 1
        with open("admin/mail.txt", "w") as mail_count_file:
            mail_count_file.write(str(h))
    else:
        bot.send_message(user_id, "<b>Error occurred while generating email</b>", parse_mode='HTML')
#
@bot.message_handler(func=lambda message: message.text == '🚀 My Email')
def get_user_email(message):
    user_id = message.from_user.id

    file_path = f"admin/mail{user_id}.json"
    if file_exists(file_path):
        email = json.load(open(file_path))['email']
        bot.send_message(user_id, f"<b>Your Email Is\n\n{email}</b>", parse_mode='HTML')
    else:
        bot.send_message(user_id, "<b>❌️ No Email created</b>", parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == '📨 Inbox')
def check_inbox(message):
    user_id = message.from_user.id

    file_path = f"admin/mail{user_id}.json"
    if file_exists(file_path):
        email = json.load(open(file_path))['email']
        response = requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages")
        if len(response.text) < 8:
            bot.send_message(user_id, "❌️ No Mail Received")
        else:
            emails = json.loads(response.text)
            for data in emails:
                msg = f"<b>Mail Received\n\nId: {data['id']}\n\nSubject: {data['subject']}\n\nText: {data['body_text']}</b>"
                bot.send_message(user_id, msg, parse_mode='HTML')
    else:
        bot.send_message(user_id, "<b>⛔️ Please Generate an email first</b>", parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == '📊  Status')
def bot_status(message):
    user_id = message.from_user.id

    tmail = int(open("admin/mail.txt").read())
    usr = int(open("admin/total.txt").read())
    img_url = "https://quickchart.io/chart?bkg=white&c={'type':'bar','data':{'labels':[''],'datasets':[{'label':'Total-Users','data':[" + str(usr) + "]},{'label':'Total-Mail Created','data':[" + str(tmail) + "]}]}}"

    caption = f"📊 Bot Live Stats 📊\n\n⚙ Total Email Generated : {tmail}\n✅️ Total Users : {usr}\n\n🔥 By: @DEVSNP"
    bot.send_photo(user_id, img_url, caption=caption)

#
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):

    if str(message.from_user.id) == admin:
        bot.send_message(message.chat.id, "Send the message you want to broadcast to all users. ✨")
        bot.register_next_step_handler(message, send_broadcast)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command. ⛔️")

#
def send_broadcast(message):
    broadcast_text = message.text
    users_directory = "admin/users/"
    user_ids = [file.split('.')[0] for file in os.listdir(users_directory)]


    for user_id in user_ids:
        try:
            bot.send_message(user_id, broadcast_text)
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")

    bot.send_message(admin, "Broadcast sent to all users! 📣")




@app.route('/')
def index():
    return "Alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()


bot.polling()

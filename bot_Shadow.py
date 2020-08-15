import time
import json 
import requests
import csv
import re
import datetime
import random
import logging
import player
import clan
import war

master_id = #Enter master chat id (Type int not string)
BOT_NAME = "BOT_NAME" # Replace with your Bot name
BOT_USERNAME = "BOT_USERNAME" # Replace with your Bot username
TOKEN = "BOT_TOKEN" # Replace with yout Bot Token
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

with open("auth.txt", "r") as f:
    authorization_key = (f.read()).strip()

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

    
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_chat_details(update):
    try:
        text = update["message"]["text"]
    except:
        text = ''
    try:
        date = update["message"]["date"]
        chat_id = update["message"]["chat"]["id"]
        sender_id = update["message"]["from"]["id"]
        message_id = update["message"]["message_id"]
    except:
        date = 0
        chat_id = 0
        sender_id = 0
        message_id = 0
    try:
        first_name = update["message"]["from"]["first_name"]
    except:
        first_name = ''
    try:
        last_name = update["message"]["from"]["last_name"]
    except:
        last_name = ''
    try:
        username = update["message"]["from"]["username"]
    except:
        username = ''

    try:
        reply_id = update["message"]["reply_to_message"]["from"]["id"]
    except:
        reply_id = ''

    try:
        reply_sticker = update["message"]["reply_to_message"]["sticker"]["file_id"]
    except:
        reply_sticker = ''

    try:
        reply_gif = update["message"]["reply_to_message"]["animation"]["file_id"]
    except:
        reply_gif = ''

    try:
        reply_pic = update["message"]["reply_to_message"]["photo"][0]["file_id"]
    except:
        reply_pic = ''

    try:
        reply_audio = update["message"]["reply_to_message"]["audio"]["file_id"]
    except:
        reply_audio = ''

    try:
        new_name = update["message"]["new_chat_member"]["first_name"]
    except:
        new_name = ''

    try:
        group_name = update["message"]["chat"]["title"]
    except:
        group_name = ''

    return (text, chat_id, sender_id, message_id, first_name, last_name, username, date, reply_id, reply_sticker, reply_gif, reply_pic, reply_audio, new_name, group_name)


def send_message(text, chat_id, reply_markup = {'remove_keyboard' : True}, **kwargs):
    url = URL + "sendMessage"
    params = {'text' : text, 'chat_id' : chat_id, 'parse_mode' : 'Markdown', 'disable_web_page_preview' : True, 'reply_markup' : json.dumps(reply_markup)}
    for key, value in kwargs.items():
        params[key] = value
    message_response = requests.get(url, params=params)
    return message_response.json()['result']['message_id']

def send_photo(photo, chat_id):
    url = URL + "sendPhoto"
    files = {'photo': photo}
    data = {'chat_id' : chat_id}
    requests.post(url, files=files, data=data)

def send_pic(pic, chat_id):
    url = URL + "sendPhoto"
    params = {'photo': pic, 'chat_id' : chat_id}
    requests.post(url, params=params)

def send_sticker(sticker, chat_id):
    url = URL + "sendSticker"
    params = {'sticker': sticker, 'chat_id' : chat_id}
    requests.post(url, params=params)

def send_gif(gif, chat_id):
    url = URL + "sendAnimation"
    params = {'animation': gif, 'chat_id' : chat_id}
    requests.post(url, params=params)

def send_audio(audio, chat_id):
    url = URL + "sendAudio"
    params = {'audio': audio, 'chat_id' : chat_id}
    requests.post(url, params=params)

def send_video(video, chat_id):
    url = URL + "sendVideo"
    params = {'video': video, 'chat_id' : chat_id}
    requests.post(url, params=params)

def send_poll(question, options, chat_id):
    url = URL + "sendPoll"
    params = {'question': question, 'options' : json.dumps(options), 'chat_id' : chat_id, 'is_anonymous' : False}
    requests.post(url, params=params)

def send_action(action, chat_id):
    url = URL + "sendChatAction"
    params = {'action': action, 'chat_id' : chat_id}
    requests.post(url, params=params)

def delete_message(chat_id, message_id):
    url = URL + "deleteMessage"
    params = {'message_id': message_id, 'chat_id' : chat_id}
    requests.get(url, params=params)

def kick_member(user_id, chat_id):
    url = URL + "kickChatMember"
    params = {'user_id': user_id, 'chat_id' : chat_id}
    resp = requests.get(url, params=params)
    if resp.json()['ok'] == True:
        return True
    elif resp.json()['ok'] == False:
        return resp.json()['description']
    else:
        return False

def mute_member(user_id, chat_id):
    url = URL + "restrictChatMember"
    permissions = json.dumps({'can_send_messages' : False, 'can_send_media_messages' : False, 'can_send_polls' : False, 'can_send_other_messages' : False, 'can_add_web_page_previews' : False, 'can_change_info' : False, 'can_invite_users' : False, 'can_pin_messages' : False})
    params = {'user_id': user_id, 'chat_id' : chat_id, 'permissions' : permissions}
    resp = requests.get(url, params=params)
    if resp.json()['ok'] == True:
        return True
    elif resp.json()['ok'] == False:
        return resp.json()['description']
    else:
        return False

def unmute_member(user_id, chat_id):
    url = URL + "restrictChatMember"
    permissions = json.dumps({'can_send_messages' : True, 'can_send_media_messages' : True, 'can_send_polls' : True, 'can_send_other_messages' : True, 'can_add_web_page_previews' : True, 'can_change_info' : True, 'can_invite_users' : True, 'can_pin_messages' : True})
    params = {'user_id': user_id, 'chat_id' : chat_id, 'permissions' : permissions}
    resp = requests.get(url, params=params)
    if resp.json()['ok'] == True:
        return True
    elif resp.json()['ok'] == False:
        return resp.json()['description']
    else:
        return False

##################################################################################
def reg_checker(first_name, last_name, sender_id, chat_id, message_id):
    with open("reg_user.csv", 'r', newline='') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            if sender_id == int(row['sender_id']):
                return True
        reply_markup = {'keyboard': [[{'text':'Ya sure, register me'}],[{'text':'Not now'}]], 'resize_keyboard': True, 'one_time_keyboard': True, 'selective':True}
        send_message("User not registered !!\nOnly registered users can set remainders and train me.\nYou can register anytime by typing /regme\nor I can register you right now if you want.",chat_id)
        send_message("Would you like to register now, [{} {}](tg://user?id={})?".format(first_name, last_name, sender_id), chat_id, reply_markup=reply_markup, reply_to_message_id=message_id)
        return False

def send_player_info(player_tag, chat_id):
    player_info_json = player.get_player_details(player_tag, authorization_key)
    player_info = player.decode(player_info_json)
    legend_info = player.decode_legend(player_info_json)
    heroes_info = player.decode_heroes(player_info_json)
    troops_info = player.decode_troops(player_info_json)
    spells_info = player.decode_spells(player_info_json)
    send_message(player_info, chat_id)
    send_message(legend_info, chat_id)
    send_message(heroes_info + '\n' + troops_info + '\n' + spells_info, chat_id)
    if player_info == "Player not found\nPlease enter valid player tag in the format\n/player <playertag>":
        return 1

def send_clan_info(clan_tag, chat_id):
    clan_info_json = clan.get_clan_details(clan_tag, authorization_key)
    clan_info = clan.decode(clan_info_json)
    members_info = clan.decode_members(clan_info_json)
    send_message(clan_info, chat_id)
    try:
        send_message('*Members:* {}\n'.format(clan_info_json['members']) + members_info, chat_id)
    except:
        pass
    if clan_info == "Clan not found\nPlease enter valid clan tag in the format\n/clan <clantag>":
        return 1

def send_war_info(clan_tag, chat_id):
    war_info_json = war.get_war_details(clan_tag, authorization_key)
    war_info = war.decode(war_info_json)
    members_info1, members_info2 = war.decode_members(war_info_json)
    opp_members_info1, opp_members_info2 = war.decode_opp_members(war_info_json)
    send_message(war_info, chat_id)
    send_message(members_info1, chat_id)
    send_message(members_info2, chat_id)
    send_message(opp_members_info1, chat_id)
    send_message(opp_members_info2, chat_id)
    if war_info == "Clan not found\nPlease enter valid clan tag in the format\n/war <clantag>":
        return 1

###############################################################################################################3

def echo_all(updates):
    for update in updates["result"]:
        try:
            text, chat_id, sender_id, message_id, first_name, last_name, username, date, reply_id, reply_sticker, reply_gif, reply_pic, reply_audio, new_name, group_name = get_chat_details(update)
            
            # Storing Bot Logs in a file
            logging.basicConfig(filename='bot_log.log',level=logging.INFO, format='%(asctime)s - | {} | {} | - {} - %(message)s'.format(sender_id, chat_id, username), datefmt='%d-%b-%y %H:%M:%S')
            logging.info(text)

            if text.lower() == "/start" or text == "/start@{}".format(BOT_USERNAME):
                send_text = "Hi {}, glad to see you here".format(first_name)
                send_message(send_text, chat_id)
                send_message("My name is {}, a clash of clans bot. I'm here to help you get any player or clan info.\n\nUse following command to get any player or clan info:\n/player <playertag> to get player details\n/clan <clantag> to get clan details\n/war <clantag> to get current war details".format(BOT_NAME), chat_id)
                send_message("If you want to register type /regme\nTo see what commands you can use type /help", chat_id)
                reply_markup = {'inline_keyboard': [[{'text':'Add to a group', 'url':'t.me/MrShadowbot?startgroup=test'}]]}
                send_message('You can even add me to a group\nTo add me to any group, click below', chat_id, reply_markup=reply_markup)
                                
            elif text.lower() == "/regme" or text == "/regme@{}".format(BOT_USERNAME):
                reply_markup = {'keyboard': [[{'text':'Yes, register me'}],[{'text':'No'}]], 'resize_keyboard': True, 'one_time_keyboard': True, 'selective':True}
                send_message("Are you sure you want to register?", chat_id, reply_markup=reply_markup, reply_to_message_id=message_id)
                
            elif text == 'Ya sure, register me' or text == 'Register Now' or text == 'Yes, register me':
                count = 0
                with open("reg_user.csv", 'r', newline='') as f:
                    f_csv = csv.DictReader(f)
                    for row in f_csv:
                        if sender_id == int(row['sender_id']):
                            count += 1
                            send_text = "User already registered!"
                            send_message(send_text, chat_id)
                            break
                    if count == 0:
                        if username == "" and text != 'Register Now':
                            send_message("Username not found !!\nLooks like you don't have a username. You can register even without username, but we prefer to have one.", chat_id)
                            reply_markup = {'keyboard': [[{'text':'Let me set username first'}],[{'text':'Register Now'}]], 'resize_keyboard': True, 'one_time_keyboard': True, 'selective':True}
                            send_message("You can go to settings to set a username or continue the registration without username", chat_id, reply_markup=reply_markup, reply_to_message_id=message_id)

                        if username != '' or text == 'Register Now':
                            with open("reg_user.csv", 'a+', newline='') as f:
                                fieldnames = ['chat_id', 'sender_id', 'username', 'first_name', 'last_name']
                                f_csv2 = csv.DictWriter(f, fieldnames=fieldnames)
                                #f_csv2.writeheader()  #use only first time if header is needed
                                f_csv2.writerow({'chat_id': chat_id, 'sender_id' : sender_id, 'username' : username, 'first_name' : first_name, 'last_name' : last_name})
                                if username != '':
                                    send_text = "User Registered\nName: {} {}\nUsername: {}\nUser ID: {}\nThanks for registration, {}".format(first_name, last_name, username, sender_id, first_name)
                                else:
                                    send_text = "User Registered\nName: {} {}\nUser ID: {}\nThanks for registration, {}".format(first_name, last_name, sender_id, first_name)
                                send_message(send_text, chat_id)

            elif text == 'Let me set username first' or text == 'No' or text == 'Not now':
                send_message("Ok", chat_id)

            elif text.lower() == "/help" or text == "/help@{}".format(BOT_USERNAME):
                reply_markup = {'inline_keyboard': [[{'text':'Join our group', 'url':'t.me/blackholeyoucantescape'}], [{'text':'Contact Admin', 'url':'t.me/Sangwan5688'}]]}
                send_message("Hey! My name is {}. I'm a clash of clans bot, here to help you get any player or clan info.\n\n*Available commands:*\n/player <playertag> : See player info\n/clan <clantag> : See clan info\n/war <clantag> : See current war info\n/regme : Register yourself\n/myinfo : Shows your info\n/botinfo : Shows Bot info".format(BOT_NAME), chat_id)
                send_message("If you have any bugs, facing any problem or have questions about me, feel free to contact Admin.", chat_id, reply_markup=reply_markup)

            elif text.lower() == "/myinfo" or text == "/myinfo@{}".format(BOT_USERNAME):
                if username != '':
                    send_text = "First Name: {}\nLast Name: {}\nUsername: {}\nChat ID: {}".format(first_name, last_name, username, sender_id)
                else:
                    send_text = "First Name: {}\nLast Name: {}\nChat ID: {}".format(first_name, last_name, sender_id)
                send_message(send_text, chat_id, reply_to_message_id=message_id)

            elif text.lower() == "/botinfo" or text == "/botinfo@{}".format(BOT_USERNAME):
                reply_markup = {'inline_keyboard': [[{'text':'Contact Admin', 'url':'t.me/Sangwan5688'}]]}
                send_text = "Botname: {}\nUsername: @{}\n\nIf you want to support me and my creator by donating a little amount of money type /donate\n".format(BOT_NAME, BOT_USERNAME) + "-"*57 + "\nMade with love by @sangwan5688" + "-"*57
                send_message(send_text, chat_id)
                send_message('Facing any problem? Have any doubts? Found bugs? Have suggestions? or any other query?\nFeel free to contact [Admin](tg://user?id={})'.format(master_id), chat_id, reply_markup=reply_markup)

            elif text.lower() == "/donate" or text == "/donate@{}".format(BOT_USERNAME):
                reply_markup = {'inline_keyboard': [[{'text':'Pay via Paypal', 'url':'https://www.paypal.me/sangwan5688'}]]}
                send_message("So you want to donate? Amazing!\nIt took a lot of work for my creator to get me where I am now. So if you have some money to spare and want to support, Donate!\nAlways nice to see my work appreciated 😊", chat_id)
                send_message("You can donate me via Paypal or UPI\nTo pay via Paypal, [click here](https://www.paypal.me/sangwan5688) or on the button below", chat_id, reply_markup=reply_markup)
                send_message("To pay by UPI, please scan the QR code", chat_id)
                send_photo(photo=open('./files/donate.jpg', 'rb'), chat_id=chat_id)
                send_message("Thank you for your support!", chat_id)

#######################################################################################
            elif text.lower()[:5] == '/poll' and sender_id == master_id:
                temp = re.match(r"(.*): (.*)", text[5:].strip())
                try:
                    question = temp.group(1)
                    options = temp.group(2).split(",")
                    send_poll(question, options, chat_id)
                except:
                    send_message("Invalid poll format", sender_id)
                delete_message(chat_id, message_id)

            elif new_name != '':
                send_message("Welcome to {}, {}\nHow are you?". format(group_name.replace('™', ''), new_name), chat_id)

            elif text.lower() == '/kick' or text == '/kick@{}'.format(BOT_USERNAME):
                if sender_id != master_id:
                    send_message('Access Denied', chat_id)

                elif reply_id != '':
                    resp = kick_member(reply_id, chat_id)
                    if resp == True:
                        send_message('[User](tg://user?id={}) Kicked'.format(reply_id), chat_id)
                    elif resp == False:
                        send_message("Error !!\nTry again later", chat_id)
                    else:
                        send_message((resp[13:]).capitalize(), chat_id)
                else:
                    send_message('User not found', chat_id)

            elif text.lower() == '/mute' or text == '/mute@{}'.format(BOT_USERNAME):
                if sender_id != master_id:
                    send_message('Access Denied', chat_id)

                elif reply_id != '':
                    resp = mute_member(reply_id, chat_id)
                    if resp == True:
                        send_message('[User](tg://user?id={}) Muted'.format(reply_id), chat_id)
                    elif resp == False:
                        send_message("Error !!\nTry again later", chat_id)
                    else:
                        send_message((resp[13:]).capitalize(), chat_id)
                    
                else:
                    send_message('User not found', chat_id)

            elif text.lower() == '/unmute' or text == '/unmute@{}'.format(BOT_USERNAME):
                if sender_id != master_id:
                    send_message('Access Denied', chat_id)

                elif reply_id != '':
                    resp = unmute_member(reply_id, chat_id)
                    if resp == True:
                        send_message('[User](tg://user?id={}) Unmuted'.format(reply_id), chat_id)
                    elif resp == False:
                        send_message("Error !!\nTry again later", chat_id)
                    else:
                        send_message((resp[13:]).capitalize(), chat_id)
                else:
                    send_message('User not found', chat_id)
                    
            elif text.lower()[:7] == '/broad ':
                if sender_id == master_id:
                    send_action(action='typing', chat_id=chat_id)
                    with open("reg_user.csv", 'r', newline='') as f:
                        f_csv = csv.DictReader(f)
                        for row in f_csv:
                            broadcast = (text[7:].strip()).replace('USERNAME', row['username'])
                            broadcast = (broadcast.replace('NAME', row['first_name'])).replace('LAST', row['last_name'])
                            send_message("{}".format(broadcast), row['sender_id'])
                        send_message('Message Broadcasted', chat_id)
                else:
                    send_message('Access Denied', chat_id)
            
            elif text.lower()[:5] == '/send':
                if sender_id == master_id:
                    id_msg = text[5:].strip()
                    pattern = r'^([-]?[0-9]+) (.*)'
                    msg_sent = re.search(pattern, id_msg)
                    send_message(msg_sent.group(2), int(msg_sent.group(1)))
                    send_message('Message Sent', chat_id)
                else:
                    send_message('Access Denied', chat_id)

            elif text.lower()[:4] == '/bh ':
                if sender_id == master_id:
                    msg = text[4:].strip()
                    send_message(msg, chat_id='-1001313125461')
                    send_message('Message Sent', chat_id)
                else:
                    send_message('Access Denied', chat_id)


########################################################################################
########################         ##      COC    ##         #############################
########################################################################################
            elif text[:7].lower() == '/player':
                if reg_checker(first_name, last_name, sender_id, chat_id, message_id):
                    player_tag = (text[7:].strip()).replace("#", "")
                    send_player_info(player_tag, chat_id)

            elif text[:19] == '/player@{}'.format(BOT_USERNAME):
                if reg_checker(first_name, last_name, sender_id, chat_id, message_id):
                    player_tag = (text[19:].strip()).replace("#", "")
                    send_player_info(player_tag, chat_id)

            elif text[:5].lower() == '/clan':
                if reg_checker(first_name, last_name, sender_id, chat_id, message_id):
                    clan_tag = (text[5:].strip()).replace("#", "")
                    send_clan_info(clan_tag, chat_id)

            elif text[:17] == '/clan@{}'.format(BOT_USERNAME):
                if reg_checker(first_name, last_name, sender_id, chat_id, message_id):
                    clan_tag = (text[17:].strip()).replace("#", "")
                    send_clan_info(clan_tag, chat_id)

            elif text[:4].lower() == '/war':
                if reg_checker(first_name, last_name, sender_id, chat_id, message_id):
                    clan_tag = (text[4:].strip()).replace("#", "")
                    send_war_info(clan_tag, chat_id)

            elif text[:16] == '/war@{}'.format(BOT_USERNAME):
                if reg_checker(first_name, last_name, sender_id, chat_id, message_id):
                    clan_tag = (text[16:].strip()).replace("#", "")
                    send_war_info(clan_tag, chat_id)

            elif text[0] == '#' or text[1] == '#':
                send_message("Undefined tag provided", chat_id)
                if reg_checker(first_name, last_name, sender_id, chat_id, message_id):
                    send_message("Searching for player with provided tag", chat_id)
                    player_tag = (text[1:].strip()).replace("#", "")
                    if send_player_info(player_tag, chat_id) == 1:
                        send_message("Searching for clan with provided tag", chat_id)
                        clan_tag = (text[1:].strip()).replace("#", "")
                        send_clan_info(clan_tag, chat_id)
                    
            elif text == '':
                continue

            else:
                send_text = random.choice(["Didn't get it", "What was that?", "Could't hear that"])
                send_message(send_text, chat_id)
                
                        

            
        except Exception as e:
            print(e)






def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

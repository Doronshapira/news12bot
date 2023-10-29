import time
import requests
from fun import initilize_bot
from datetime import datetime
import pytz

# Replace 'YOUR_BOT_TOKEN' with the actual token you obtained from the BotFather
TOKEN = '6864884396:AAEvwSSrNmF3prXUxMhDjPsVjw-ZlMsRHyw'

# Replace 'YOUR_CHAT_ID' with the actual chat ID you want to send messages to
CHAT_ID = '-1002097430141'


# Variable to keep track of the maximum processed message ID
last_message_unix = 0
message_dict = initilize_bot()

def subtract_dicts(dict1, dict2):
    # Create a new dictionary to store the elements that didn't appear in the first dictionary
    result_dict = {}
    # Iterate through the items in the second dictionary
    for key, value in dict1.items():
        # Check if the key is not present in the first dictionary
        if key not in dict2:
            # Add the key-value pair to the result dictionary
            result_dict[key] = value

    return result_dict
def send_message(message_details):
    chat_id = CHAT_ID
    media=message_details['Media Type']
    if media:
        requests.post(f'https://api.telegram.org/bot{TOKEN}/send{media}',
                                 params={'chat_id': chat_id, media.lower(): message_details['Media URL'],
                                         'caption': message_details['Message']})
    else:
        # Create the message text without the time
        message_text = f"{message_details['Reporter Name']}\n" \
                       f"{message_details['Message']}"
    # Send the message to the specified chat
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                             params={'chat_id': chat_id, 'text': message_text, 'parse_mode': 'Markdown'})

def msg_id_to_unix(message_details):
    il_timezone = pytz.timezone('Israel')
    # Get the current date and time in Israel time
    current_time_il = datetime.now(il_timezone)
    formatted_time = current_time_il.strftime("%Y-%m-%d")
    time = message_details['Time']
    # Convert the time string to a datetime object
    datetime_object = datetime.strptime(formatted_time + ' {}'.format(time), "%Y-%m-%d %H:%M")
    # Convert the datetime object to a Unix timestamp
    unix_timestamp = int(datetime_object.timestamp())
    return unix_timestamp
def update_channel(last_dict):
    global last_message_unix  # Use the global variable
    # For demonstration purposes, let's update a sample message in message_dict
    message_dict = initilize_bot()
    result = subtract_dicts(message_dict, last_dict)
    # Send updates to the channel for the new messages
    for msg_id, message_details in result.items():
        last_update=msg_id_to_unix(message_details)
        # Check if the message has already been sent based on message ID
        if int(last_update) > last_message_unix:
            last_message_unix=int(last_update)
            send_message(message_details)
            time.sleep(1)  # To avoid rate limiting, you can adjust this as needed


def main():
    print('start')
    global last_message_unix
    global message_dict
    # Set up the scheduler for background task
    while True:
        try:
            update_channel(message_dict)
        except Exception as e:
            print(e)
        time.sleep(10)  # Update every 60 seconds


if __name__ == '__main__':
    main()

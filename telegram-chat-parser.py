import sys
import csv
import json
from datetime import datetime

if len(sys.argv) != 3:
    print("ERROR: incorrect number of arguments!")
    print("How to use it:")
    print("    python3 telegram-chat-parser.py <chat_history_json> <output_csv>")
    print("Example:")
    print("    python3 telegram-chat-parser.py movies_group.json chat_movies.csv")
    sys.exit()

result_filepath = sys.argv[1]
output_filepath = sys.argv[2]
columns = ["msg_id",
            "sender",
            "sender_id",
            "reply_to_msg_id",
            "date",
            "msg_type",
            "msg_content",
            "has_mention",
            "has_email",
            "has_phone",
            "has_hashtag",
            "is_bot_command"]

file_types = ["animation",
              "video_file",
              "video_message",
              "voice_message",
              "audio_file"]

mention_types = ["mention",
                 "mention_name"]



with open(result_filepath, encoding='utf8') as input_file:
    telegram_export = json.load(input_file)

available_chat_names = [chat['name'] for chat in telegram_export['chats']['list'] if ('name' in chat) and chat['name'] != None]


n = 0

for i in available_chat_names:

    output = "csv/" + f'{i}' + output_filepath

    with open(result_filepath, "r", encoding="utf-8") as infile:
        with open(output, "w", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, columns, dialect="unix", quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            
            contents = infile.read()

            jdata = json.loads(contents)

            obj = jdata["chats"]["list"][n]

            for message in obj["messages"]:
                if message["type"] != "message":
                    continue
                
                msg_id = message["id"]
                sender = message["from"]
                sender_id = message["from_id"]
                reply_to_msg_id = message["reply_to_message_id"] if "reply_to_message_id" in message else -1
                date = message["date"].replace("T", " ")
                dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                
                msg_content = message["text"]
                msg_type = "text"
                
                if "media_type" in message:
                    msg_type = message["media_type"]
                    if message["media_type"] == "sticker":
                        if "sticker_emoji" in message:
                            msg_content = message["file"]
                        else:
                            msg_content = "?"
                    elif message["media_type"] in file_types:
                        msg_content = message["file"]
                elif "file" in message:
                    msg_type = "file"
                    msg_content = message["file"]
                
                if "photo" in message:
                    msg_type = "photo"
                    msg_content = message["photo"]
                elif "poll" in message:
                    msg_type = "poll"
                    msg_content = str(message["poll"]["total_voters"])
                elif "location_information" in message:
                    msg_type = "location"
                    loc = message["location_information"]
                    msg_content = str(loc["latitude"]) + "," + str(loc["longitude"])
                
                has_mention = 0
                has_email = 0
                has_phone = 0
                has_hashtag = 0
                is_bot_command = 0
                
                if type(msg_content) == list:
                    txt_content = ""
                    for part in msg_content:
                        if type(part) == str:
                            txt_content += part
                        elif type(part) == dict:
                            if part["type"] == "link":
                                msg_type = "link"
                            elif part["type"] in mention_types:
                                has_mention = 1
                            elif part["type"] == "email":
                                has_email = 1
                            elif part["type"] == "phone":
                                has_phone = 1
                            elif part["type"] == "hashtag":
                                has_hashtag = 1
                            elif part["type"] == "bot_command":
                                is_bot_command = 1
                            
                            txt_content += part["text"]
                    msg_content = txt_content
                
                msg_content = msg_content.replace("\n", " ")
                
                row = {
                    "msg_id"          : msg_id,
                    "sender"          : sender,
                    "sender_id"       : sender_id,
                    "reply_to_msg_id" : reply_to_msg_id,
                    "date"            : date,
                    "msg_type"        : msg_type,
                    "msg_content"     : msg_content,
                    "has_mention"     : has_mention,
                    "has_email"       : has_email,
                    "has_phone"       : has_phone,
                    "has_hashtag"     : has_hashtag,
                    "is_bot_command"  : is_bot_command,
                }
                
                writer.writerow(row)

    n += 1

""" telegrama_chat_parser.py

author       : Artur Rodrigues Rocha Neto
email        : artur.rodrigues26@gmail.com
github       : https://github.com/keizerzilla
created      : 23/december/2020
description  : Script to parse a Telegram chat history JSON file into CSV tabular format.
details      : This script is a way to parse the most (but not all) of the Telegram Data Export Schema.
reference    : https://core.telegram.org/import-export
requirements : Python 3.x

You can use this file as an executable script or importing the TelegramChatParser class in your project.
Have fun! I hope this little program helps you! (:

- Artur
"""

import csv
import json
import argparse

from datetime import datetime

def timestamp():
    """ [AUXILIARY] Generates string with current timestamp.
    
    Returns
    -------
        stamp: datetime string in '%Y-%m-%d_%H-%M-%S' format. 
    """
    
    now = datetime.now()
    stamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    return stamp

def debug(msg):
    """ [AUXILIARY] Simple debug function with runtime timestamp.
    
    Parameters
    ----------
        msg: Developer text to be shown in the default output.
    """
    
    print(f"DEBUG | {timestamp()} | {msg}")

class TelegramChatParser:
    """ The full chat parser abstraction in the form of a class.
    """
    
    def __init__(self):
        """ Le constructor.
        """
        
        self.columns = [
            "msg_id",
            "sender",
            "sender_id",
            "reply_to_msg_id",
            "date",
            "date_unixtime",
            "msg_type",
            "msg_content",
            "forwarded_from",
            "action",
            "has_mention",
            "has_email",
            "has_phone",
            "has_hashtag",
            "is_bot_command",
        ]
        
        self.file_types = [
            "animation",
            "video_file",
            "video_message",
            "voice_message",
            "audio_file",
        ]
        
        self.mention_types = [
            "mention",
            "mention_name",
        ]
    
    def process_message(self, message):
        """ Parses the contents of a Telegram 'Message' object.
        
        Parameters
        ----------
            message: a dictionary in the structure of a 'Message' object.
        
        Returns
        -------
            parsed_row: a row ready to be stored in the CSV.
        """
        
        if message["type"] != "message":
            return None
        
        msg_id = message["id"]
        sender = message["from"]
        sender_id = message["from_id"]
        date = message["date"]
        date_unixtime = message["date_unixtime"]
        
        reply_to_msg_id = message.get("reply_to_message_id", "")
        action = message.get("action", "")
        forwarded_from = message.get("forwarded_from", "")
        
        has_mention = 0
        has_email = 0
        has_phone = 0
        has_hashtag = 0
        is_bot_command = 0
        
        msg_content = message.get("text", "")
        msg_type = "text"
        
        if "media_type" in message:
            msg_type = message["media_type"]
            if message["media_type"] == "sticker":
                if "sticker_emoji" in message:
                    msg_content = message["file"]
                else:
                    msg_content = "?"
            elif message["media_type"] in self.file_types:
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
            msg_content = f"{loc['latitude']},{loc['longitude']}"
        
        if isinstance(msg_content, list):
            txt_content = ""
            for part in msg_content:
                if isinstance(part, str):
                    txt_content += part
                elif isinstance(part, dict):
                    if part["type"] == "link":
                        msg_type = "link"
                    elif part["type"] in self.mention_types:
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
        
        parsed_row = {
            "msg_id"          : msg_id,
            "sender"          : sender,
            "sender_id"       : sender_id,
            "reply_to_msg_id" : reply_to_msg_id,
            "date"            : date,
            "date_unixtime"   : date_unixtime,
            "msg_type"        : msg_type,
            "msg_content"     : msg_content,
            "forwarded_from"  : forwarded_from,
            "action"          : action,
            "has_mention"     : has_mention,
            "has_email"       : has_email,
            "has_phone"       : has_phone,
            "has_hashtag"     : has_hashtag,
            "is_bot_command"  : is_bot_command,
        }
        
        return parsed_row
    
    def process_chat(self, jdata):
        """ Parses the contents of a 'Chat' object.
        
        Parameters
        ----------
            jdata: a dictionary in the structure of a 'Chat' object.
        """
        
        chat = jdata["name"]
        
        rows = []
        for message in jdata["messages"]:
            row = self.process_message(message)
            if row is not None:
                rows.append(row)
        
        dump = {
            "chat" : chat,
            "rows" : rows,
        }
        
        debug(f"{chat} parsed ok!")
        
        return dump
    
    def process(self, chat_history_json):
        """ Parses a exported file.
        
        Parameters
        ----------
            chat_history_json: path to 'result.json' created by Telegram Desktop.
        """
        
        with open(chat_history_json, "r", encoding="utf-8-sig") as input_file:
            contents = input_file.read()
            jdata = json.loads(contents)
            
            if "chats" in jdata:
                return [self.process_chat(chat) for chat in jdata["chats"]["list"]]
            elif "left_chats" in jdata:
                return [self.process_chat(chat) for chat in jdata["left_chats"]["list"]]
            else:
                return [self.process_chat(jdata)]
    
    def to_csv(self, data, include_timestamp=False):
        """ Saves the parsed data to CSV files, one for each chat exported.
        The filename with match the chat name with optional timestamp.
        
        Parameters
        ----------
            data: list of parsed chats.
            include_timestamp: if True, puts a timestamp in the filename.
        """
        
        for dump in data:
            output_filepath = f"{dump['chat']}.csv"
            
            if include_timestamp:
                output_filepath = f"{timestamp()}_{output_filepath}"
            
            with open(output_filepath, "w", encoding="utf-8-sig", newline="") as output_file:
                writer = csv.DictWriter(output_file, self.columns, dialect="unix", quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                
                for row in dump["rows"]:
                    writer.writerow(row)

if __name__ == "__main__":
    """ Usage as executable script.
    
    Example
    -------
        python3 telegram_chat_parser.py <result.json_filepath>
    """
    
    parser = argparse.ArgumentParser(
        prog="telegram_chat_parser.py",
        description="Script to parse a Telegram chat history JSON file into CSV tabular format.",
        usage="python3 telegram_chat_parser.py result.json -o my_chat_data.csv",
        epilog="Post issues at https://github.com/keizerzilla/telegram-chat-parser/issues"
    )
    
    parser.add_argument("chat_history_json", help="'result.json' file path of exported chat history.")
    
    args = vars(parser.parse_args())
    chat_history_json = args["chat_history_json"]
    
    parser = TelegramChatParser()
    data = parser.process(chat_history_json)
    parser.to_csv(data)

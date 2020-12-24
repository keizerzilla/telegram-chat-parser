"""
file:         telegram-chat-parser.py
author:       Artur Rodrigues Rocha Neto
email:        artur.rodrigues26@gmail.com
github:       https://github.com/keizerzilla
created:      23/12/2020
description:  Script to parse a Telegram chat history JSON file into a tabular format (CSV).
requirements: Python 3.x
"""

import sys
import csv
import json

if len(sys.argv) != 3:
    print("ERROR: incorrect number of arguments!")
    print("How to:")
    print("    python3 telegram-chat-parser.py <chat_history_json> <output_csv>")
    print("Example:")
    print("    python3 telegram-chat-parser.py movies_group.json chat_movies.csv")
    sys.exit()

result_filepath = sys.argv[1]
output_filepath = sys.argv[2]
template = ["id", "from", "from_id", "reply_to_message_id", "date", "text"]

with open(result_filepath, "r", encoding="utf-8") as infile:
    with open(output_filepath, "w", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, template, dialect="unix", quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        
        contents = infile.read()
        jdata = json.loads(contents)
        
        for message in jdata["messages"]:
            if message["type"] != "message" or len(message["text"]) == 0:
                continue
            
            id_ = message["id"]
            from_ = message["from"]
            from_id_ = message["from_id"]
            reply_to_message_id_ = message["reply_to_message_id"] if "reply_to_message_id" in message else -1
            date_ = message["date"]
            text_ = message["text"]
            
            if type(text_) == list:
                new_text = ""
                for part in text_:
                    if type(part) == str:
                        new_text += part
                    elif type(part) == dict:
                        new_text += part["text"]
                text_ = new_text
            
            text_ = text_.replace("\n", " ")
            
            row = {
                "id"                  : id_,
                "from"                : from_,
                "from_id"             : from_id_,
                "reply_to_message_id" : reply_to_message_id_,
                "date"                : date_,
                "text"                : text_,
            }
            
            writer.writerow(row)

print("Parse of {} into {} finished!".format(result_filepath, output_filepath))

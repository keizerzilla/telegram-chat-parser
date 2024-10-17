# telegram-chat-parser

Python script to parse a Telegram chat history backup (`JSON`) into tabular format (`CSV`). No extra packages required, only Python 3.x!

## How to use it

Using Telegram's Desktop or Web interfaces, go to the chat you want to backup, click on the options button (three dots in the upper right corner) and them click on `Export chat history`. In the dialog window, right next to `Format`, chose `JSON`. After the backup is completed, Telegram will generate a `result.json` file. This will be the input of our script.

Next, navigate to the directory where the `result.json` is located and make sure that the script is accessible, probably by placing it next to the results file. Then, run the script by typing:

```python
python3 telegram_chat_parser.py result.json
```

For each chat backup in `result.json`, a `.csv` file will be created in the same directory. The output filename is a stripped down version of the actual chat name (only letters and numbers are kept).

## Using with other Python functions

You can use the base parser defined in the `TelegramChatParser` class as well. A simple example:

```python
from telegram_chat_parser import TelegramChatParser

parser = TelegramChatParser()
data = parser.process("result.json")
parser.to_csv(data)
```

## The output format

Once the script is done parsing, the result `CSV` file will have the format bellow:

- `msg_id`: the unique identifier of the message.
- `sender`: the literal name of the sender.
- `sender_id`: the unique identifier of the sender.
- `reply_to_mesg_id`: if the message is a reply, this column will store the id of that message.
- `date`: date time stamp of the message.
- `msg_type`:  can be one of the following: `text`, `sticker`, `file`, `photo`, `poll`, `location` or `link`.
- `msg_content`: the text content the message, already cleaned in terms of newline and spaces; if the message was not a text (sticker, media, etc) this field will store the path pointing to the media.
- `has_mention`: it will be `1` if there's a mention in the text, `0` otherwise.
- `has_email`: it will be `1` if there's a email in the text, `0` otherwise.
- `has_phone`: it will be `1` if there's a phone contact in the message, `0` otherwise.
- `has_hashtag`: it will be `1` if there's a hashtag in the text, `0` otherwise.
- `is_bot_command`: it will be `1` if the message is a bot command, `0` otherwise.

If multiples chat had been exported, one `CSV` will be created for each chat, named after the respective chat names.

## Contributing

I hope this little script helps you in your project! If you have any suggestions or ideas to improve it, please feel free to open an issue. Thank you!

## Projects

If you used this script in a project (paper, study, analysis, etc), feel free to use this space as a way to share it! Create a issue, post a description of the project with a link to it and I will edit this README with it.

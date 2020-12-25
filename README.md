# telegram-chat-parser

Python script to parse a Telegram chat history backup (`JSON`) into tabular format (`CSV`). No extra packages required, only Python 3.x!

## How to use it

Using Telegram's Desktop or Web interfaces, go to the chat you want to backup, click on the options button (three dots in the upper right corner) and them click on `Export chat history`. In the dialog window, right next to `Format`, chose `JSON`. After the backup is completed, Telegram will generate a `results.json` file. This will be the input of our script.

Next, navigate to the directory where the `results.json` is located and make sure that the script is accessible, probably by placing it next to the results file. Then, run the script by typing:

```python
python3 telegram-chat-parser.py results.json dump.csv
```

In the example above, we chose `dump.csv` as the file which the parsed data will be stored, but you can name it whatever you want. The script has no output indicating it's done and should work everytime quite fast, even for large chats, as long as Telegram doesn't change it's format for backups.

## The output format

Once the script is done parsing, the result `CSV` file will have the format bellow:

| id | from | from_id | reply_to_message_id | date | text | media_type |
|----|------|---------|---------------------|------|------|------------|

 - `id`: the unique identifier of the message
 - `from`: the literal name of the sender
 - `from_id`: the unique identifier of the sender
 - `reply_to_message_id`: if the message is a reply, this column will store the id of that message, or -1 otherwise
 - `date`: date time stamp of the message
 - `text`: the text content the message, already cleaned in terms of newline and spaces; if the message was not a text (sticker, media, etc) this field will store a empty string
 - `media_type`: if the message was some sort of media, this column will have its type, or an empty string otherwise

## Contributing

I hope this little script helps you in your project! If you have any suggestions or ideas to improve it, please feel free to open an issue. Thank you!

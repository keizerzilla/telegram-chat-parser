# telegram-chat-parser

Python script to parse a Telegram chat history backup (`JSON`) into tabular format (`CSV`). No extra packages required, only Python 3.x!

## How to use it

Using Telegram's Desktop or Web interfaces, go to the chat you want to backup, click on the options button (three dots in the upper right corner) and them click on `Export chat history`. In the dialog window, right next to `Format`, chose `JSON`. After the backup is complete, Telegram will generate a `results.json` file. This is will the input of our script.

Next, navigate to the directory where the `results.json` is located and run the script using:

```python
python3 telegram-chat-parser.py results.json dump.csv
```

In the example above, we chose `dump.csv` as the file which the dataset will be stored, but you can name it whatever you want. The script has no output indicating it's done and should work everytime, as long as Telegram doesn't change it's format for backups.

## Contributing

I hope this little script helps you in your project! If you have any suggestions, critics or ideas to improve it, please feel free to open an issue. Thanks!

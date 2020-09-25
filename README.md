# TeleNex

TeleNex is a Python library for easy making telegram bots

## Usage

```python
from TeleNex import Bot

bot = Bot('<tocken>')

@bot.on_message( cmds=['start'] )
def start(msg):
  bot.send_msg('Bot started! :D')
  
bot.run()
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

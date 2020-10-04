# TeleNex

TeleNex is a Python library for easy making telegram bots

## Usage

```python
from teleNex import Bot

bot = Bot('<tocken>')

@bot.on_message( cmds=['start'] )
def start(msg):
  bot.send_msg('Bot started! :D')
  
bot.run()
```

## Installation
```
pip install teleNex
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

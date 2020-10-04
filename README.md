# TeleNex

TeleNex is a Python library for easy making telegram bots

____

## Usage

```python
from teleNex import Bot

bot = Bot('<tocken>')

@bot.on_message( cmds=['start'] )
def start(msg):
  bot.send_msg('Bot started! :D')
  
bot.run()
```

____

## Installation
```
pip install teleNex
```

____

## Documentation


### About Bot class
Bot is the main TeleNex class. To import it you have to write:
```python
from teleNex import Bot
```
This class contains all the necessary functions (which will be discussed further) for sending or receiving messages

To create a bot object, you need to write:
```python
bot = Bot('<tocken>')
```
<token> is a unique token for your bot. Can be obtained from @BotFather

To launch the bot, use the run function:
```python
bot.run()
```

____

## License

[MIT](https://choosealicense.com/licenses/mit/)

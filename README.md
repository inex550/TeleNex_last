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
[About Bot class](#about-bot-class)

[Methods](#methods)
> [send_msg](#send_msg)

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
\<tocken\> is a unique token for your bot. Can be obtained from @BotFather

To launch the bot, use the run function:
```python
bot.run()
```

### Methods

#### send_msg

The send_msg method is used to send text messages. For instance:
```python
bot.send_msg('I'm the bot :D')
```

By default, the message will be sent to the chat from which the last message was received

You can also explicitly specify the chat_id and then the message will be sent to the desired chat. For instance:
```python
bot.send_msg('I'm the bot :D', chat_id=<chat id>)
```
\<chat id\> - **integer** value - identifier of chat

You can also add a keyboard option. For instance:
```python
bot.send_msg('I'm the bot :D', keyboard=keyboard_object)
```
How to create a keyboard object is described [here](#keyboard)
____

## License

[MIT](https://choosealicense.com/licenses/mit/)

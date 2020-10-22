# TeleNex

TeleNex это Python модуль лёгкого создания Telegram ботов

____

## Использование

```python
from teleNex import Bot

bot = Bot('<tocken>')

@bot.on_message( cmds=['start'] )
def start(msg):
  bot.send_msg('Bot started! :D')
  
bot.run()
```

____

## Установка
```
pip install teleNex
```

____

## Документация
[Про Bot class](#about-bot-class)

[Методы](#методы)
> [send_msg](#send_msg)
> [send_sticker](#send_sticker)
> [send_image](#send_image)
> [send_audio](#send_audio)
[Типы](#)
> [Message](#Message)
> [InlineKeyboard](#InlineKeyboard)
> [ReplyKeyboard](#ReplyKeyboard)

### Про Bot клас
Bot это главный класс TeleNex, при помощи него отправляются сообщения и файлы. 
Импортировать его можно так:
```python
from teleNex import Bot
```

Создать объект бота можно так:
```python
bot = Bot('<tocken>')
```
\<tocken\> уникальный индентификатор бота. Можно получить у @BotFather

Чтобы запустить бота, используйте функцию run:
```python
bot.run()
```

### Методы

#### send_msg

Для отправки сообщений используется метод send_msg. Например:
```python
bot.send_msg('I am the bot :D')
```

По умолчанию сообщение отправляется в чат, из которого было получено последнее сообщение
Но вы так же можете явно указать id чата, в который хотите отправить сообщение при помощи параметры chat_id:
```python
bot.send_msg('I am the bot :D', chat_id=<chat id>)
```
\<chat id\> - Целочисленное значение - идентификатор чата

Вы так же можете добавить параметр keyboard для отправки клавиатуры:
```python
bot.send_msg('I am the bot :D', keyboard=keyboard_object)
```
Как создать клавиатуру рассказано [здесь](#keyboard)
____

## License

[MIT](https://choosealicense.com/licenses/mit/)
